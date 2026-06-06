"""
models/transformer.py — GPT-like Transformer Language Model (Small Scale)
Phụ trách: Thành viên 3 (TV3)

Kiến trúc:
  Embedding → N × TransformerBlock (MHA + FFN + LayerNorm) → LM Head

Config mặc định:
  n_layers=4, n_heads=4, d_model=256, d_ff=1024
  vocab_size=50257 (GPT-2 tokenizer)
  Tổng tham số: ~10M

Độ phức tạp Self-Attention: O(L²) per layer
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F


class CausalSelfAttention(nn.Module):
    """
    Multi-Head Causal Self-Attention.

    Tính: Attention(Q,K,V) = softmax(QKᵀ / √d_head) · V
    Causal mask đảm bảo token tại vị trí t chỉ attend vào t' ≤ t.

    Complexity: O(L²·d) per forward pass — đây là bottleneck chính.
    """

    def __init__(self, d_model: int, n_heads: int,
                 max_seq_len: int, dropout: float = 0.1):
        super().__init__()
        assert d_model % n_heads == 0, "d_model phải chia hết cho n_heads"

        self.n_heads = n_heads
        self.d_head = d_model // n_heads
        self.scale = math.sqrt(self.d_head)

        # Q, K, V projections (gộp thành 1 linear để tối ưu)
        self.qkv_proj = nn.Linear(d_model, 3 * d_model, bias=False)
        self.out_proj = nn.Linear(d_model, d_model, bias=False)
        self.attn_dropout = nn.Dropout(dropout)
        self.resid_dropout = nn.Dropout(dropout)

        # Causal mask: lower triangular (chỉ attend vào quá khứ)
        # register_buffer: lưu mask nhưng không coi là parameter
        causal_mask = torch.tril(
            torch.ones(max_seq_len, max_seq_len, dtype=torch.bool)
        )
        self.register_buffer("causal_mask", causal_mask)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: (B, L, d_model)
        Returns:
            out: (B, L, d_model)
        """
        B, L, D = x.shape

        # Tính Q, K, V cùng lúc: (B, L, 3D) → split thành 3 × (B, L, D)
        q, k, v = self.qkv_proj(x).split(D, dim=-1)

        # Reshape thành multi-head: (B, n_heads, L, d_head)
        def split_heads(t):
            return t.view(B, L, self.n_heads, self.d_head).transpose(1, 2)

        q, k, v = split_heads(q), split_heads(k), split_heads(v)

        # Scaled dot-product attention: O(L² · d_head)
        # attn_scores: (B, n_heads, L, L)
        attn_scores = (q @ k.transpose(-2, -1)) / self.scale

        # Áp dụng causal mask: vị trí trong tương lai → -inf → softmax → 0
        mask = self.causal_mask[:L, :L]  # Crop theo L thực tế
        attn_scores = attn_scores.masked_fill(~mask, float("-inf"))

        # Softmax + dropout
        attn_weights = F.softmax(attn_scores, dim=-1)
        attn_weights = self.attn_dropout(attn_weights)

        # Weighted sum: (B, n_heads, L, d_head)
        out = attn_weights @ v

        # Merge heads: (B, L, D)
        out = out.transpose(1, 2).contiguous().view(B, L, D)
        return self.resid_dropout(self.out_proj(out))


class FeedForward(nn.Module):
    """
    Position-wise Feed-Forward Network.
    FFN(x) = Linear(GELU(Linear(x)))
    Complexity: O(L · d_model · d_ff)
    """

    def __init__(self, d_model: int, d_ff: int, dropout: float = 0.1):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(d_ff, d_model),
            nn.Dropout(dropout),
        )

    def forward(self, x):
        return self.net(x)


class TransformerBlock(nn.Module):
    """
    1 Transformer Block = Pre-LN + Attention + Pre-LN + FFN + Residuals.

    Dùng Pre-LayerNorm (trước attention/FFN) vì ổn định hơn khi train.
    """

    def __init__(self, d_model: int, n_heads: int, d_ff: int,
                 max_seq_len: int, dropout: float = 0.1):
        super().__init__()
        self.ln1 = nn.LayerNorm(d_model)
        self.attn = CausalSelfAttention(d_model, n_heads, max_seq_len, dropout)
        self.ln2 = nn.LayerNorm(d_model)
        self.ffn = FeedForward(d_model, d_ff, dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Pre-LN Attention với residual
        x = x + self.attn(self.ln1(x))
        # Pre-LN FFN với residual
        x = x + self.ffn(self.ln2(x))
        return x


class TransformerLM(nn.Module):
    """
    GPT-like Causal Language Model dựa trên Transformer.

    Architecture:
      Token Embedding + Positional Embedding
      → N × TransformerBlock
      → LayerNorm
      → Linear LM Head (vocab projection)

    Total complexity per forward pass: O(N · L² · d_model)
    """

    def __init__(
        self,
        vocab_size: int = 50257,
        d_model: int = 256,
        n_layers: int = 4,
        n_heads: int = 4,
        d_ff: int = 1024,
        max_seq_len: int = 1024,
        dropout: float = 0.1,
    ):
        super().__init__()
        self.d_model = d_model
        self.max_seq_len = max_seq_len

        # Embeddings
        self.token_emb = nn.Embedding(vocab_size, d_model)
        self.pos_emb = nn.Embedding(max_seq_len, d_model)
        self.emb_dropout = nn.Dropout(dropout)

        # Transformer blocks
        self.blocks = nn.ModuleList([
            TransformerBlock(d_model, n_heads, d_ff, max_seq_len, dropout)
            for _ in range(n_layers)
        ])

        # Final LayerNorm + LM Head
        self.ln_f = nn.LayerNorm(d_model)
        self.lm_head = nn.Linear(d_model, vocab_size, bias=False)

        # Weight tying: embedding và lm_head dùng chung weight (tiết kiệm tham số)
        self.lm_head.weight = self.token_emb.weight

        # Khởi tạo weights
        self.apply(self._init_weights)

    def _init_weights(self, module):
        """Khởi tạo theo GPT-2: Normal(0, 0.02)."""
        if isinstance(module, (nn.Linear, nn.Embedding)):
            nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if isinstance(module, nn.Linear) and module.bias is not None:
                nn.init.zeros_(module.bias)
        elif isinstance(module, nn.LayerNorm):
            nn.init.ones_(module.weight)
            nn.init.zeros_(module.bias)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: (B, L) — token ids

        Returns:
            logits: (B, L, vocab_size)
        """
        B, L = x.shape
        assert L <= self.max_seq_len, \
            f"Sequence length {L} vượt max_seq_len {self.max_seq_len}"

        # Token + positional embedding
        positions = torch.arange(L, device=x.device)
        h = self.emb_dropout(self.token_emb(x) + self.pos_emb(positions))

        # Qua N Transformer blocks
        for block in self.blocks:
            h = block(h)

        # Final norm + project to vocab
        h = self.ln_f(h)
        logits = self.lm_head(h)
        return logits

    def count_parameters(self) -> int:
        """Đếm số tham số trainable."""
        return sum(p.numel() for p in self.parameters() if p.requires_grad)


# ─── Quick Test ─────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Testing TransformerLM ===")
    model = TransformerLM(
        vocab_size=50257,
        d_model=256,
        n_layers=4,
        n_heads=4,
        d_ff=1024,
        max_seq_len=1024,
    )
    print(f"Parameters: {model.count_parameters():,}")

    # Test forward pass
    B, L = 4, 256
    x = torch.randint(0, 50257, (B, L))
    logits = model(x)
    print(f"Input:  {x.shape}")
    print(f"Output: {logits.shape}")  # Expect (4, 256, 50257)
    assert logits.shape == (B, L, 50257)
    print("✅ TransformerLM forward pass OK!")
