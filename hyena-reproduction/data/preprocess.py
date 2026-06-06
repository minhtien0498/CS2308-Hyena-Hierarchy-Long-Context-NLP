"""
data/preprocess.py — WikiText-2 Data Pipeline
Phụ trách: Thành viên 2 (TV2)

Chức năng:
  - Load WikiText-2 từ HuggingFace
  - Tokenize bằng GPT-2 tokenizer (BPE)
  - Tạo SequenceDataset và DataLoader theo seq_len

Usage:
  python data/preprocess.py --seq_len 256 --split train
  python data/preprocess.py --seq_len 512 --split validation
"""

import argparse
import os
import torch
from torch.utils.data import Dataset, DataLoader
from datasets import load_dataset
from transformers import GPT2Tokenizer


# ─── Constants ────────────────────────────────────────────────
DATASET_NAME = "wikitext"
DATASET_CONFIG = "wikitext-2-raw-v1"
TOKENIZER_NAME = "gpt2"
CACHE_DIR = ".cache"


# ─── Dataset Class ─────────────────────────────────────────────
class SequenceDataset(Dataset):
    """
    Tạo dataset bằng cách cắt chuỗi token thành các đoạn seq_len.
    Mỗi sample: (x, y) với x = token[i:i+seq_len], y = token[i+1:i+seq_len+1]
    (language modeling: dự đoán token tiếp theo)
    """
    def __init__(self, tokens: torch.Tensor, seq_len: int):
        self.tokens = tokens
        self.seq_len = seq_len
        # Số sample = số lần chia hết (bỏ phần dư cuối)
        self.n_samples = (len(tokens) - 1) // seq_len

    def __len__(self):
        return self.n_samples

    def __getitem__(self, idx):
        start = idx * self.seq_len
        x = self.tokens[start : start + self.seq_len]
        y = self.tokens[start + 1 : start + self.seq_len + 1]
        return x, y


# ─── Core Functions ────────────────────────────────────────────
def load_tokenizer(cache_dir: str = CACHE_DIR) -> GPT2Tokenizer:
    """Load GPT-2 BPE tokenizer (tải về lần đầu, cache lại sau)."""
    os.makedirs(cache_dir, exist_ok=True)
    local_path = os.path.join(cache_dir, "gpt2_tokenizer")
    if os.path.exists(local_path):
        print(f"[Tokenizer] Loading from cache: {local_path}")
        return GPT2Tokenizer.from_pretrained(local_path)
    print(f"[Tokenizer] Downloading {TOKENIZER_NAME}...")
    tokenizer = GPT2Tokenizer.from_pretrained(TOKENIZER_NAME)
    tokenizer.save_pretrained(local_path)
    return tokenizer


def load_and_tokenize(split: str = "train",
                      tokenizer: GPT2Tokenizer = None) -> torch.Tensor:
    """
    Load WikiText-2 và tokenize thành tensor 1D.

    Args:
        split: 'train', 'validation', hoặc 'test'
        tokenizer: GPT2Tokenizer instance

    Returns:
        torch.Tensor shape (N,) với N là tổng số tokens
    """
    print(f"[Dataset] Loading WikiText-2 split='{split}'...")
    dataset = load_dataset(DATASET_NAME, DATASET_CONFIG, split=split)

    # Ghép tất cả văn bản thành 1 chuỗi (bỏ dòng trống)
    all_text = "\n".join(
        [line for line in dataset["text"] if line.strip() != ""]
    )

    print(f"[Dataset] Total characters: {len(all_text):,}")
    print(f"[Tokenizer] Encoding...")

    # Encode: text → list of int token ids
    token_ids = tokenizer.encode(all_text)
    tokens = torch.tensor(token_ids, dtype=torch.long)

    print(f"[Dataset] Total tokens ({split}): {len(tokens):,}")
    return tokens


def get_dataloader(split: str = "train",
                   seq_len: int = 256,
                   batch_size: int = 16,
                   num_workers: int = 0) -> DataLoader:
    """
    Trả về DataLoader sẵn dùng cho training/evaluation.

    Args:
        split: 'train', 'validation', hoặc 'test'
        seq_len: độ dài chuỗi (256, 512, 1024, ...)
        batch_size: batch size (giảm nếu OOM)
        num_workers: số worker process (0 = main process, an toàn trên Colab)

    Returns:
        torch.utils.data.DataLoader
    """
    tokenizer = load_tokenizer()
    tokens = load_and_tokenize(split, tokenizer)
    seq_dataset = SequenceDataset(tokens, seq_len)

    loader = DataLoader(
        seq_dataset,
        batch_size=batch_size,
        shuffle=(split == "train"),   # Chỉ shuffle khi train
        num_workers=num_workers,
        pin_memory=True,
    )

    print(f"[DataLoader] split={split} | seq_len={seq_len} | "
          f"batch_size={batch_size} | batches={len(loader):,}")
    return loader


def get_dataset_stats(tokenizer: GPT2Tokenizer = None):
    """In thống kê dataset: số token, vocab size."""
    if tokenizer is None:
        tokenizer = load_tokenizer()

    stats = {}
    for split in ["train", "validation", "test"]:
        tokens = load_and_tokenize(split, tokenizer)
        stats[split] = {
            "n_tokens": len(tokens),
            "vocab_size": tokenizer.vocab_size,
        }

    print("\n" + "="*50)
    print("WIKITEXT-2 STATISTICS")
    print("="*50)
    print(f"{'Split':<15} {'Tokens':>12} {'Vocab':>10}")
    print("-"*40)
    for split, info in stats.items():
        print(f"{split:<15} {info['n_tokens']:>12,} {info['vocab_size']:>10,}")
    print("="*50)
    return stats


# ─── Synthetic Task (Bonus) ─────────────────────────────────────
class AssociativeRecallDataset(Dataset):
    """
    Synthetic associative recall task để kiểm tra long-context.

    Format input: [k1→v1, k2→v2, ..., kN→vN, query: kq→?]
    Label: vq

    Ví dụ:
      Input tokens: [A, 1, B, 2, C, 3, B, ?]
      Target: 2
    """
    def __init__(self, n_samples: int = 1000,
                 seq_len: int = 256,
                 vocab_size: int = 64,
                 n_pairs: int = None):
        self.n_samples = n_samples
        self.seq_len = seq_len
        self.vocab_size = vocab_size
        # Số cặp key-value trong mỗi sequence
        self.n_pairs = n_pairs or (seq_len // 4)

    def __len__(self):
        return self.n_samples

    def __getitem__(self, idx):
        torch.manual_seed(idx)  # Reproducible
        # Tạo n_pairs cặp (key, value)
        keys = torch.randint(0, self.vocab_size // 2, (self.n_pairs,))
        values = torch.randint(self.vocab_size // 2, self.vocab_size, (self.n_pairs,))
        # Query: chọn 1 key ngẫu nhiên
        query_idx = torch.randint(0, self.n_pairs, (1,)).item()
        query_key = keys[query_idx]
        target = values[query_idx]
        # Xây dựng sequence: [k1, v1, k2, v2, ..., query_key, SEP]
        pairs = torch.stack([keys, values], dim=1).flatten()   # (2*n_pairs,)
        sep_token = self.vocab_size  # Token đặc biệt
        x = torch.cat([pairs, torch.tensor([query_key, sep_token])])
        # Pad hoặc truncate đến seq_len
        if len(x) < self.seq_len:
            x = torch.cat([x, torch.zeros(self.seq_len - len(x), dtype=torch.long)])
        else:
            x = x[:self.seq_len]
        return x, target


# ─── CLI Entry Point ────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WikiText-2 Data Pipeline")
    parser.add_argument("--seq_len", type=int, default=256,
                        help="Sequence length (default: 256)")
    parser.add_argument("--split", type=str, default="train",
                        choices=["train", "validation", "test"],
                        help="Dataset split")
    parser.add_argument("--batch_size", type=int, default=16,
                        help="Batch size (default: 16)")
    parser.add_argument("--stats", action="store_true",
                        help="Chỉ in thống kê dataset, không tạo dataloader")
    args = parser.parse_args()

    if args.stats:
        get_dataset_stats()
    else:
        loader = get_dataloader(
            split=args.split,
            seq_len=args.seq_len,
            batch_size=args.batch_size
        )
        # Kiểm tra một batch
        x, y = next(iter(loader))
        print(f"\n[Check] x.shape={x.shape}, y.shape={y.shape}")
        print(f"[Check] x dtype={x.dtype}, range=[{x.min()}, {x.max()}]")
        print("✅ Dataloader hoạt động bình thường!")
