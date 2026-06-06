"""
train.py — Training Loop chính
Phụ trách: Thành viên 3 (TV3)

Chức năng:
  - Load dataset WikiText-2
  - Khởi tạo model (Transformer hoặc Hyena)
  - Train với AdamW + Cosine LR Scheduler
  - Save checkpoint tốt nhất
  - Log metrics ra CSV

Usage:
  # Train Transformer
  python train.py --model transformer --seq_len 256 --epochs 20

  # Train Hyena
  python train.py --model hyena --seq_len 256 --epochs 20

  # Chạy nhanh để test (2 epoch)
  python train.py --model transformer --seq_len 128 --epochs 2 --batch_size 4
"""

import os
import sys
import time
import math
import argparse
import csv
from datetime import datetime

import torch
import torch.nn as nn
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingLR

# Import models và data pipeline
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from models import TransformerLM, HyenaLM
from data.preprocess import get_dataloader


# ─── Config ────────────────────────────────────────────────────
MODEL_CONFIGS = {
    "transformer": {
        "vocab_size": 50257,
        "d_model": 256,
        "n_layers": 4,
        "n_heads": 4,
        "d_ff": 1024,
        "dropout": 0.1,
    },
    "hyena": {
        "vocab_size": 50257,
        "d_model": 256,
        "n_layers": 4,
        "order": 2,
        "filter_dim": 64,
        "d_ff": 1024,
        "dropout": 0.1,
    },
}

TRAIN_DEFAULTS = {
    "lr": 3e-4,
    "weight_decay": 0.1,
    "beta1": 0.9,
    "beta2": 0.95,
    "grad_clip": 1.0,
    "warmup_ratio": 0.05,    # 5% số steps đầu để warmup LR
}


# ─── Utility Functions ──────────────────────────────────────────
def get_device():
    """Chọn device tốt nhất có sẵn."""
    if torch.cuda.is_available():
        device = torch.device("cuda")
        print(f"[Device] GPU: {torch.cuda.get_device_name(0)}")
    elif torch.backends.mps.is_available():
        device = torch.device("mps")
        print("[Device] Apple MPS (M1/M2)")
    else:
        device = torch.device("cpu")
        print("[Device] CPU (sẽ chạy chậm hơn)")
    return device


def build_model(model_name: str, max_seq_len: int, device: torch.device):
    """Khởi tạo model theo tên."""
    config = MODEL_CONFIGS[model_name].copy()
    config["max_seq_len"] = max_seq_len

    if model_name == "transformer":
        model = TransformerLM(**config)
    elif model_name == "hyena":
        model = HyenaLM(**config)
    else:
        raise ValueError(f"Unknown model: {model_name}. Chọn 'transformer' hoặc 'hyena'")

    model = model.to(device)
    n_params = model.count_parameters()
    print(f"[Model] {model_name.upper()} | Parameters: {n_params:,} ({n_params/1e6:.1f}M)")
    return model


def compute_loss(model, batch, device):
    """Tính cross-entropy loss cho 1 batch."""
    x, y = batch
    x, y = x.to(device), y.to(device)
    logits = model(x)
    # logits: (B, L, V), y: (B, L)
    # Flatten để tính cross-entropy: (B*L, V) vs (B*L,)
    loss = nn.functional.cross_entropy(
        logits.view(-1, logits.size(-1)),
        y.view(-1),
        ignore_index=-1
    )
    return loss


def get_peak_memory_mb() -> float:
    """Lấy peak GPU memory (MB), trả về 0 nếu không có GPU."""
    if torch.cuda.is_available():
        return torch.cuda.max_memory_allocated() / 1024**2
    return 0.0


def linear_warmup_cosine_decay(step: int, warmup_steps: int, total_steps: int,
                                min_lr_ratio: float = 0.1) -> float:
    """
    LR schedule: linear warmup → cosine decay.
    Trả về multiplier để nhân với base LR.
    """
    if step < warmup_steps:
        return step / max(1, warmup_steps)
    progress = (step - warmup_steps) / max(1, total_steps - warmup_steps)
    cosine_val = 0.5 * (1 + math.cos(math.pi * progress))
    return min_lr_ratio + (1 - min_lr_ratio) * cosine_val


# ─── Training Loop ──────────────────────────────────────────────
def train(args):
    """Main training function."""
    device = get_device()

    # ── Setup output directory ──
    os.makedirs("results/checkpoints", exist_ok=True)
    os.makedirs("results", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_name = f"{args.model}_L{args.seq_len}_{timestamp}"
    checkpoint_path = f"results/checkpoints/{run_name}_best.pt"
    csv_path = f"results/E1_{args.model}_L{args.seq_len}.csv"

    print(f"\n{'='*60}")
    print(f"  Run: {run_name}")
    print(f"  Model: {args.model} | Seq len: {args.seq_len}")
    print(f"  Epochs: {args.epochs} | Batch size: {args.batch_size}")
    print(f"{'='*60}\n")

    # ── Load data ──
    print("[Data] Loading train dataloader...")
    train_loader = get_dataloader(
        split="train", seq_len=args.seq_len, batch_size=args.batch_size
    )
    print("[Data] Loading validation dataloader...")
    val_loader = get_dataloader(
        split="validation", seq_len=args.seq_len, batch_size=args.batch_size
    )

    # ── Build model ──
    model = build_model(args.model, args.seq_len, device)

    # ── Optimizer ──
    # Weight decay chỉ áp dụng cho weight matrices, không cho bias/LayerNorm
    decay_params = [p for n, p in model.named_parameters()
                    if p.requires_grad and p.dim() >= 2]
    no_decay_params = [p for n, p in model.named_parameters()
                       if p.requires_grad and p.dim() < 2]
    optimizer = AdamW([
        {"params": decay_params, "weight_decay": TRAIN_DEFAULTS["weight_decay"]},
        {"params": no_decay_params, "weight_decay": 0.0},
    ], lr=args.lr, betas=(TRAIN_DEFAULTS["beta1"], TRAIN_DEFAULTS["beta2"]))

    # ── LR Schedule ──
    total_steps = len(train_loader) * args.epochs
    warmup_steps = int(TRAIN_DEFAULTS["warmup_ratio"] * total_steps)
    print(f"[Train] Total steps: {total_steps:,} | Warmup steps: {warmup_steps:,}")

    # ── CSV Logger ──
    csv_file = open(csv_path, "w", newline="")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([
        "epoch", "train_loss", "val_loss", "val_ppl",
        "train_time_s", "peak_mem_mb", "lr"
    ])

    # ── Training ──
    best_val_loss = float("inf")
    global_step = 0

    for epoch in range(1, args.epochs + 1):
        model.train()
        epoch_loss = 0.0
        epoch_start = time.time()
        if torch.cuda.is_available():
            torch.cuda.reset_peak_memory_stats()

        for batch_idx, batch in enumerate(train_loader):
            # LR warmup/decay theo step
            lr_mult = linear_warmup_cosine_decay(global_step, warmup_steps, total_steps)
            for group in optimizer.param_groups:
                group["lr"] = args.lr * lr_mult

            # Forward + backward
            optimizer.zero_grad()
            loss = compute_loss(model, batch, device)
            loss.backward()

            # Gradient clipping (tránh exploding gradients)
            nn.utils.clip_grad_norm_(model.parameters(), TRAIN_DEFAULTS["grad_clip"])

            optimizer.step()
            epoch_loss += loss.item()
            global_step += 1

            # Progress log mỗi 50 batches
            if (batch_idx + 1) % 50 == 0:
                avg_loss = epoch_loss / (batch_idx + 1)
                print(f"  Epoch {epoch}/{args.epochs} | "
                      f"Step {batch_idx+1}/{len(train_loader)} | "
                      f"Loss: {avg_loss:.4f} | "
                      f"LR: {args.lr * lr_mult:.2e}")

        # ── Epoch metrics ──
        train_loss = epoch_loss / len(train_loader)
        train_time = time.time() - epoch_start
        peak_mem = get_peak_memory_mb()
        current_lr = args.lr * linear_warmup_cosine_decay(
            global_step, warmup_steps, total_steps
        )

        # ── Validation ──
        val_loss = evaluate_loss(model, val_loader, device)
        val_ppl = math.exp(min(val_loss, 20))  # Cap ở 20 để tránh overflow

        # ── Logging ──
        print(f"\n[Epoch {epoch:2d}/{args.epochs}] "
              f"Train Loss: {train_loss:.4f} | "
              f"Val Loss: {val_loss:.4f} | "
              f"Val PPL: {val_ppl:.2f} | "
              f"Time: {train_time:.1f}s | "
              f"Mem: {peak_mem:.0f}MB")

        csv_writer.writerow([
            epoch, f"{train_loss:.6f}", f"{val_loss:.6f}",
            f"{val_ppl:.4f}", f"{train_time:.2f}",
            f"{peak_mem:.1f}", f"{current_lr:.6f}"
        ])
        csv_file.flush()

        # ── Save best checkpoint ──
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save({
                "epoch": epoch,
                "model_state_dict": model.state_dict(),
                "optimizer_state_dict": optimizer.state_dict(),
                "val_loss": val_loss,
                "config": MODEL_CONFIGS[args.model],
                "args": vars(args),
            }, checkpoint_path)
            print(f"  💾 Saved best checkpoint (val_loss={val_loss:.4f})")

    csv_file.close()
    print(f"\n✅ Training complete!")
    print(f"   Best val loss: {best_val_loss:.4f} (PPL: {math.exp(best_val_loss):.2f})")
    print(f"   Results saved: {csv_path}")
    print(f"   Checkpoint: {checkpoint_path}")
    return best_val_loss


def evaluate_loss(model, val_loader, device) -> float:
    """Tính average loss trên validation set."""
    model.eval()
    total_loss = 0.0
    n_batches = 0
    with torch.no_grad():
        for batch in val_loader:
            loss = compute_loss(model, batch, device)
            total_loss += loss.item()
            n_batches += 1
    model.train()
    return total_loss / max(1, n_batches)


# ─── Argument Parsing ───────────────────────────────────────────
def parse_args():
    parser = argparse.ArgumentParser(
        description="Train Transformer hoặc Hyena trên WikiText-2"
    )
    parser.add_argument(
        "--model", type=str, default="transformer",
        choices=["transformer", "hyena"],
        help="Model để train (default: transformer)"
    )
    parser.add_argument(
        "--seq_len", type=int, default=256,
        help="Sequence length (default: 256). Thử 512, 1024 cho E2/E3"
    )
    parser.add_argument(
        "--epochs", type=int, default=20,
        help="Số epoch training (default: 20)"
    )
    parser.add_argument(
        "--batch_size", type=int, default=16,
        help="Batch size (default: 16). Giảm nếu OOM"
    )
    parser.add_argument(
        "--lr", type=float, default=3e-4,
        help="Learning rate (default: 3e-4)"
    )
    return parser.parse_args()


# ─── Entry Point ────────────────────────────────────────────────
if __name__ == "__main__":
    args = parse_args()
    train(args)
