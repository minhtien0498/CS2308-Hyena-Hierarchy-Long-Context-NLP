"""
evaluate.py — Evaluation Script
Phụ trách: Thành viên 3 (TV3)

Chức năng:
  - Load checkpoint đã train
  - Tính validation/test loss và perplexity
  - Đo training time per step (để so sánh E2/E3)
  - Đo GPU memory (nếu có)
  - Export kết quả ra CSV

Usage:
  # Evaluate một model
  python evaluate.py --model transformer --seq_len 256

  # So sánh scaling (E2/E3): đo time/memory theo seq_len
  python evaluate.py --model transformer --scaling --seq_lens 256 512 1024
  python evaluate.py --model hyena --scaling --seq_lens 256 512 1024 2048
"""

import os
import sys
import time
import math
import argparse
import csv

import torch
import torch.nn as nn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from models import TransformerLM, HyenaLM
from data.preprocess import get_dataloader


# ─── Utility ────────────────────────────────────────────────────
def get_device():
    if torch.cuda.is_available():
        return torch.device("cuda")
    elif torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def load_model_from_checkpoint(checkpoint_path: str, model_name: str,
                                seq_len: int, device: torch.device):
    """Load model từ checkpoint."""
    from models import TransformerLM, HyenaLM
    from train import MODEL_CONFIGS, build_model

    checkpoint = torch.load(checkpoint_path, map_location=device)
    model = build_model(model_name, seq_len, device)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()
    print(f"[Checkpoint] Loaded from: {checkpoint_path}")
    print(f"  Best val loss: {checkpoint.get('val_loss', 'N/A'):.4f}")
    return model


def build_model_fresh(model_name: str, seq_len: int, device: torch.device):
    """Khởi tạo model mới (dùng cho scaling test mà không cần checkpoint)."""
    configs = {
        "transformer": dict(vocab_size=50257, d_model=256, n_layers=4,
                            n_heads=4, d_ff=1024, max_seq_len=seq_len, dropout=0.0),
        "hyena": dict(vocab_size=50257, d_model=256, n_layers=4,
                      order=2, filter_dim=64, d_ff=1024,
                      max_seq_len=seq_len, dropout=0.0),
    }
    if model_name == "transformer":
        model = TransformerLM(**configs["transformer"])
    else:
        model = HyenaLM(**configs["hyena"])
    return model.to(device)


# ─── Evaluation Functions ────────────────────────────────────────
def evaluate_perplexity(model, data_loader, device) -> dict:
    """
    Tính val/test loss và perplexity.

    Returns:
        dict với keys: loss, perplexity
    """
    model.eval()
    total_loss = 0.0
    n_batches = 0

    with torch.no_grad():
        for x, y in data_loader:
            x, y = x.to(device), y.to(device)
            logits = model(x)
            loss = nn.functional.cross_entropy(
                logits.view(-1, logits.size(-1)), y.view(-1)
            )
            total_loss += loss.item()
            n_batches += 1

    avg_loss = total_loss / max(1, n_batches)
    perplexity = math.exp(min(avg_loss, 20))  # Cap để tránh overflow

    return {"loss": avg_loss, "perplexity": perplexity}


def measure_time_and_memory(model, seq_len: int, batch_size: int,
                             device: torch.device, n_warmup: int = 5,
                             n_measure: int = 20) -> dict:
    """
    Đo thời gian forward pass và GPU memory.

    Args:
        n_warmup: Số bước warmup (không tính vào kết quả)
        n_measure: Số bước đo thực tế

    Returns:
        dict với: time_per_step_ms, peak_mem_mb, throughput_tokens_per_sec
    """
    model.eval()
    dummy_x = torch.randint(0, 50257, (batch_size, seq_len), device=device)

    # Warmup
    with torch.no_grad():
        for _ in range(n_warmup):
            _ = model(dummy_x)

    # Reset memory stats
    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()
        torch.cuda.synchronize()

    # Measure
    times = []
    with torch.no_grad():
        for _ in range(n_measure):
            start = time.perf_counter()
            _ = model(dummy_x)
            if torch.cuda.is_available():
                torch.cuda.synchronize()  # Đợi GPU hoàn thành
            elapsed = time.perf_counter() - start
            times.append(elapsed * 1000)  # Convert sang ms

    avg_time_ms = sum(times) / len(times)
    tokens_per_step = batch_size * seq_len
    throughput = tokens_per_step / (avg_time_ms / 1000)  # tokens/sec

    peak_mem_mb = 0.0
    if torch.cuda.is_available():
        peak_mem_mb = torch.cuda.max_memory_allocated() / 1024**2

    return {
        "time_per_step_ms": avg_time_ms,
        "peak_mem_mb": peak_mem_mb,
        "throughput_tokens_per_sec": throughput,
    }


# ─── Scaling Analysis (E2/E3) ───────────────────────────────────
def run_scaling_experiment(model_name: str, seq_lens: list, batch_size: int,
                            device: torch.device, output_csv: str):
    """
    Chạy scaling experiment: đo time/memory theo seq_len.
    Dùng cho E2 (Transformer) và E3 (Hyena).
    """
    print(f"\n{'='*60}")
    print(f"  Scaling Experiment: {model_name.upper()}")
    print(f"  Seq lengths: {seq_lens}")
    print(f"{'='*60}")

    results = []
    print(f"\n{'Seq Len':>10} | {'Time (ms)':>12} | {'Mem (MB)':>10} | {'Throughput (tok/s)':>20}")
    print("-" * 60)

    for seq_len in seq_lens:
        try:
            model = build_model_fresh(model_name, seq_len, device)
            metrics = measure_time_and_memory(model, seq_len, batch_size, device)

            row = {
                "model": model_name,
                "seq_len": seq_len,
                "time_ms": metrics["time_per_step_ms"],
                "peak_mem_mb": metrics["peak_mem_mb"],
                "throughput": metrics["throughput_tokens_per_sec"],
            }
            results.append(row)

            print(f"{seq_len:>10} | "
                  f"{metrics['time_per_step_ms']:>12.2f} | "
                  f"{metrics['peak_mem_mb']:>10.1f} | "
                  f"{metrics['throughput_tokens_per_sec']:>20.0f}")

            # Giải phóng memory
            del model
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

        except RuntimeError as e:
            if "out of memory" in str(e).lower():
                print(f"{seq_len:>10} | {'OOM':>12} | {'OOM':>10} | {'OOM':>20}")
                results.append({
                    "model": model_name, "seq_len": seq_len,
                    "time_ms": "OOM", "peak_mem_mb": "OOM", "throughput": "OOM"
                })
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
            else:
                raise e

    # Save CSV
    with open(output_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(f"\n💾 Saved: {output_csv}")
    return results


# ─── Main ───────────────────────────────────────────────────────
def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate Language Models")
    parser.add_argument("--model", type=str, required=True,
                        choices=["transformer", "hyena"])
    parser.add_argument("--seq_len", type=int, default=256)
    parser.add_argument("--batch_size", type=int, default=8)
    parser.add_argument("--split", type=str, default="validation",
                        choices=["validation", "test"])
    parser.add_argument("--checkpoint", type=str, default=None,
                        help="Path to checkpoint. Nếu không có, dùng model mới")
    parser.add_argument("--scaling", action="store_true",
                        help="Chạy scaling experiment thay vì evaluate perplexity")
    parser.add_argument("--seq_lens", nargs="+", type=int,
                        default=[256, 512, 1024],
                        help="Danh sách seq_len cho scaling experiment")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    device = get_device()

    os.makedirs("results", exist_ok=True)

    if args.scaling:
        # ── Scaling Experiment (E2/E3) ──
        output_csv = f"results/E{'2' if args.model == 'transformer' else '3'}_{args.model}_scale.csv"
        results = run_scaling_experiment(
            args.model, args.seq_lens, args.batch_size, device, output_csv
        )

    else:
        # ── Perplexity Evaluation (E1) ──
        print(f"\n[Evaluate] Model={args.model} | Seq={args.seq_len} | Split={args.split}")

        if args.checkpoint and os.path.exists(args.checkpoint):
            model = load_model_from_checkpoint(
                args.checkpoint, args.model, args.seq_len, device
            )
        else:
            print("[Warning] Không tìm thấy checkpoint — dùng model chưa train")
            model = build_model_fresh(args.model, args.seq_len, device)

        loader = get_dataloader(args.split, args.seq_len, args.batch_size)
        metrics = evaluate_perplexity(model, loader, device)
        time_metrics = measure_time_and_memory(model, args.seq_len, args.batch_size, device)

        print(f"\n{'='*50}")
        print(f"  Model:       {args.model.upper()}")
        print(f"  Seq Length:  {args.seq_len}")
        print(f"  Val Loss:    {metrics['loss']:.4f}")
        print(f"  Perplexity:  {metrics['perplexity']:.2f}")
        print(f"  Time/step:   {time_metrics['time_per_step_ms']:.2f} ms")
        print(f"  Peak Memory: {time_metrics['peak_mem_mb']:.1f} MB")
        print(f"{'='*50}\n")
