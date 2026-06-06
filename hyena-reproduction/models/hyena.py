"""
models/hyena.py — Hyena Language Model (Small Scale, Pure PyTorch)
Phụ trách: Thành viên 3 (TV3)

Kiến trúc Hyena (Poli et al., ICML 2023):
  Recurrence: z^(n+1)_t = x^n_t · (h^n * z^n)_t   với n=1,...,N
  Output: y = z^(N+1)

Hai thành phần cốt lõi:
  1. Implicit Long Convolution: h_t = Window(t) · FFN(PosEnc(t))
     → filter dài L với số tham số nhỏ → tách biệt memory và params
  2. Element-wise Gating: x^n · conv_output
     → data-controlled filtering → tương tự vai trò Q,K,V trong attention

Complexity: O(N · L log₂ L) vs Attention O(L²)
  → Hyena nhanh hơn khi L lớn

Implementation note:
  Dùng PyTorch thuần (torch.fft.rfft) thay vì CUDA kernel tùy chỉnh
  → Đủ để demo xu hướng, không cần GPU đặc biệt
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F


class PositionalEncoding(nn.Module):
    """
    Sinusoidal positional encoding dùng để parametrize Hyena filter.

    Công thức:
      PE(t, 2i)   = sin(t · ω_i)
      PE(t, 2i+1) = cos(t · ω_i)
    với ω_i = exp(i · log(max_freq) / (dim/2))

    Output shape: (L, emb_dim)
    """

    def __init__(self, emb_dim: int = 64, max_freq: float = 1e4):
        super().__init__()
        self.emb_dim = emb_dim
        self.max_freq = max_freq

    def forward(self, L: int, device: torch.device) -> torch.Tensor:
        # t ∈ [0, 1], shape (L, 1)
        t = torch.linspace(0, 1, L, device=device).unsqueeze(-1)
        # Tần số log-spaced: shape (emb_dim/2,)
        freqs = torch.exp(
            torch.linspace(
                0, math.log(self.max_freq),
                self.emb_dim // 2, device=device
            )
        )
        # Sinusoidal encoding: shape (L, emb_dim)
        enc = torch.cat([
            torch.sin(t * freqs),
            torch.cos(t * freqs)
        ], dim=-1)
        return enc


class HyenaFilter(nn.Module):
    """
    Implicit Long Convolution Filter via FFN.

    Công thức: h_t = Window(t) · FFN(PositionalEncoding(t))

    Ưu điểm:
      - Filter length = L (toàn bộ sequence) nhưng số tham số chỉ là O(filter_dim)
      - Tách biệt memory (L) khỏi parameter count
      - Có thể học filter dạng exponential decay, high-frequency, v.v.

    Args:
        d_model: Số channel
        order: Số bước recurrence N (Hyena^N)
        filter_dim: Số neuron hidden trong FFN
        max_seq_len: Độ dài sequence tối đa
    """

    def __init__(
        self,
        d_model: int,
        order: int = 2,
        filter_dim: int = 64,
        max_seq_len: int = 1024,
    ):
        super().__init__()
        self.order = order
        self.d_model = d_model

        # Positional encoding cho input của FFN
        self.pos_enc = PositionalEncoding(emb_dim=filter_dim)

        # FFN: PositionalEncoding(t) → filter values cho tất cả N orders và D channels
        # Input dim: filter_dim, Output dim: N * d_model
        self.ffn = nn.Sequential(
            nn.Linear(filter_dim, filter_dim),
            nn.SiLU(),             # Smooth activation (tốt cho filter learning)
            nn.Linear(filter_dim, order * d_model),
        )

        # Learnable exponential decay window: Window(t) = exp(-decay · t)
        # Mỗi order và channel có decay rate riêng
        # log_decay để đảm bảo decay > 0 sau exp
        self.log_decay = nn.Parameter(
            torch.randn(order, d_model) * 0.1
        )

        # Bias thêm vào window để filter không bị zero ở đuôi
        self.bias = nn.Parameter(torch.zeros(order, d_model))

    def forward(self, L: int) -> torch.Tensor:
        """
        Tính filter h cho sequence length L.

        Returns:
            h: (order, d_model, L) — N filters, mỗi filter dài L
        """
        device = self.log_decay.device

        # 1. Positional encoding: shape (L, filter_dim)
        t_enc = self.pos_enc(L, device)

        # 2. FFN: (L, filter_dim) → (L, order * d_model)
        h = self.ffn(t_enc)

        # 3. Reshape: (L, order, d_model) → (order, d_model, L)
        h = h.view(L, self.order, self.d_model).permute(1, 2, 0)

        # 4. Áp dụng exponential decay window
        # t: (L,), decay: (order, d_model) → window: (order, d_model, L)
        t = torch.linspace(0, 1, L, device=device)
        decay = torch.exp(-torch.exp(self.log_decay))  # (order, d_model)
        window = decay.unsqueeze(-1) ** t.unsqueeze(0).unsqueeze(0)  # broadcasting
        # Thêm bias để filter không bị collapse về 0
        h = h * window + self.bias.unsqueeze(-1) * (1 - window)

        return h  # (order, d_model, L)


class HyenaOperator(nn.Module):
    """
    Hyena Operator: thực hiện N bước recurrence.

    Recurrence:
      z^0 = v  (projection của input)
      z^(n+1) = x^n · FFTConv(h^n, z^n)   với n = 0,...,N-1
      output = z^N

    Mỗi bước kết hợp:
      - FFTConv: long-range memory (global context qua filter h^n)
      - Gating x^n: data-controlled selection (tương tự vai trò Q, K trong attention)

    Args:
        d_model: Số channel
        order: N — số bước recurrence
        filter_dim: Kích thước hidden FFN trong filter
        max_seq_len: Độ dài sequence tối đa
        dropout: Dropout rate
    """

    def __init__(
        self,
        d_model: int,
        order: int = 2,
        filter_dim: int = 64,
        max_seq_len: int = 1024,
        dropout: float = 0.1,
    ):
        super().__init__()
        self.order = order
        self.d_model = d_model

        # Input projection: u ∈ R^D → (N+1) gates: x^1,...,x^N, v
        # +1 vì cần cả v (initial value) và N gates
        self.input_proj = nn.Linear(d_model, (order + 1) * d_model, bias=False)

        # Short depthwise conv trước recurrence (giúp capture local context)
        self.short_conv = nn.Conv1d(
            in_channels=(order + 1) * d_model,
            out_channels=(order + 1) * d_model,
            kernel_size=3, padding=2, groups=(order + 1) * d_model
        )

        # Implicit long filter
        self.hyena_filter = HyenaFilter(d_model, order, filter_dim, max_seq_len)

        # Output projection
        self.out_proj = nn.Linear(d_model, d_model, bias=False)
        self.dropout = nn.Dropout(dropout)

    def _causal_fft_conv(self, h: torch.Tensor, v: torch.Tensor) -> torch.Tensor:
        """
        Causal convolution via FFT: y = h * v (causal).

        Dùng zero-padding 2L để thực hiện linear (aperiodic) convolution,
        sau đó lấy L phần tử đầu để đảm bảo causality.

        Complexity: O(L log L) nhờ FFT
        Compared to direct convolution: O(L²)

        Args:
            h: (B, D, L) hoặc (D, L) — filter
            v: (B, D, L) — signal

        Returns:
            y: (B, D, L)
        """
        L = v.shape[-1]
        fft_len = 2 * L  # Zero-padding cho linear convolution

        # FFT cả hai (real FFT: nhanh hơn complex FFT)
        H = torch.fft.rfft(h, n=fft_len, dim=-1)
        V = torch.fft.rfft(v, n=fft_len, dim=-1)

        # Convolution = pointwise multiplication trong frequency domain
        Y = H * V

        # Inverse FFT + lấy L phần tử đầu (causal)
        y = torch.fft.irfft(Y, n=fft_len, dim=-1)[..., :L]
        return y

    def forward(self, u: torch.Tensor) -> torch.Tensor:
        """
        Args:
            u: (B, L, d_model)
        Returns:
            out: (B, L, d_model)
        """
        B, L, D = u.shape

        # 1. Input projection: (B, L, D) → (B, L, (N+1)·D)
        projected = self.input_proj(u)  # (B, L, (N+1)*D)

        # 2. Short causal conv (capture local patterns)
        # Conv1d cần (B, C, L)
        projected = projected.transpose(1, 2)  # (B, (N+1)*D, L)
        projected = self.short_conv(projected)[..., :L]  # Causal crop
        projected = projected.transpose(1, 2)  # (B, L, (N+1)*D)

        # 3. Tách thành N gates và v
        # Shape mỗi phần: (B, L, D)
        parts = projected.chunk(self.order + 1, dim=-1)
        # parts[-1] là v (initial value), parts[0..N-1] là gates x^0,...,x^(N-1)
        gates = list(parts[:-1])  # [x^0, ..., x^(N-1)], mỗi cái (B, L, D)
        v = parts[-1]             # (B, L, D)

        # Chuyển sang (B, D, L) cho FFT
        z = v.transpose(1, 2)     # (B, D, L)
        gate_tensors = [g.transpose(1, 2) for g in gates]  # list of (B, D, L)

        # 4. Tính implicit filters: (order, D, L)
        h_all = self.hyena_filter(L)

        # 5. Hyena Recurrence
        # z^(n+1) = x^n · FFTConv(h^n, z^n)
        for n in range(self.order):
            h_n = h_all[n]           # (D, L)
            x_n = gate_tensors[n]    # (B, D, L)
            conv = self._causal_fft_conv(h_n, z)  # (B, D, L)
            z = x_n * conv           # element-wise: (B, D, L)

        # 6. Output projection
        out = z.transpose(1, 2)      # (B, L, D)
        return self.dropout(self.out_proj(out))


class HyenaBlock(nn.Module):
    """
    1 Hyena Block = Pre-LN + HyenaOperator + Pre-LN + FFN + Residuals.

    Cùng cấu trúc tổng quan với TransformerBlock nhưng thay MHA bằng HyenaOperator.
    Cho phép so sánh công bằng khi giữ nguyên n_layers, d_model, d_ff.
    """

    def __init__(
        self,
        d_model: int,
        order: int = 2,
        filter_dim: int = 64,
        d_ff: int = 1024,
        max_seq_len: int = 1024,
        dropout: float = 0.1,
    ):
        super().__init__()
        self.ln1 = nn.LayerNorm(d_model)
        self.hyena = HyenaOperator(d_model, order, filter_dim, max_seq_len, dropout)
        self.ln2 = nn.LayerNorm(d_model)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(d_ff, d_model),
            nn.Dropout(dropout),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x + self.hyena(self.ln1(x))   # Hyena với residual
        x = x + self.ffn(self.ln2(x))      # FFN với residual
        return x


class HyenaLM(nn.Module):
    """
    Hyena Language Model — thay thế MHA trong GPT bằng HyenaOperator.

    Giữ nguyên:
      - Token + Positional Embedding
      - N × Block structure
      - LayerNorm + LM Head
      - Weight tying

    Thay thế:
      - CausalSelfAttention (O(L²)) → HyenaOperator (O(N·L log L))

    Total complexity per forward pass: O(N_layers · N_order · L log L · d_model)
    """

    def __init__(
        self,
        vocab_size: int = 50257,
        d_model: int = 256,
        n_layers: int = 4,
        order: int = 2,
        filter_dim: int = 64,
        d_ff: int = 1024,
        max_seq_len: int = 1024,
        dropout: float = 0.1,
    ):
        super().__init__()
        self.d_model = d_model
        self.max_seq_len = max_seq_len

        # Embeddings (giống Transformer)
        self.token_emb = nn.Embedding(vocab_size, d_model)
        self.pos_emb = nn.Embedding(max_seq_len, d_model)
        self.emb_dropout = nn.Dropout(dropout)

        # Hyena blocks
        self.blocks = nn.ModuleList([
            HyenaBlock(d_model, order, filter_dim, d_ff, max_seq_len, dropout)
            for _ in range(n_layers)
        ])

        # Final norm + LM head
        self.ln_f = nn.LayerNorm(d_model)
        self.lm_head = nn.Linear(d_model, vocab_size, bias=False)

        # Weight tying
        self.lm_head.weight = self.token_emb.weight

        # Init weights
        self.apply(self._init_weights)

    def _init_weights(self, module):
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
        assert L <= self.max_seq_len

        positions = torch.arange(L, device=x.device)
        h = self.emb_dropout(self.token_emb(x) + self.pos_emb(positions))

        for block in self.blocks:
            h = block(h)

        h = self.ln_f(h)
        return self.lm_head(h)

    def count_parameters(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)


# ─── Quick Test ─────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Testing HyenaLM ===")
    model = HyenaLM(
        vocab_size=50257,
        d_model=256,
        n_layers=4,
        order=2,
        filter_dim=64,
        d_ff=1024,
        max_seq_len=1024,
    )
    print(f"Parameters: {model.count_parameters():,}")

    B, L = 4, 256
    x = torch.randint(0, 50257, (B, L))
    logits = model(x)
    print(f"Input:  {x.shape}")
    print(f"Output: {logits.shape}")  # Expect (4, 256, 50257)
    assert logits.shape == (B, L, 50257)
    print("✅ HyenaLM forward pass OK!")

    # Test FFT convolution properties
    print("\n=== Testing FFT Convolution ===")
    op = HyenaOperator(d_model=64, order=2)
    u = torch.randn(2, 128, 64)  # (B, L, D)
    out = op(u)
    print(f"HyenaOperator: {u.shape} → {out.shape}")
    assert out.shape == u.shape
    print("✅ HyenaOperator forward pass OK!")
