# Kế Hoạch Triển Khai Thực Tế — Đề Tài Hyena Hierarchy
**Nhóm:** 3 thành viên · **Thời gian:** 3 tuần · **Môn:** CS2308 – Chuyên đề NLP
**Bài báo:** *Hyena Hierarchy: Towards Larger Convolutional Language Models* (Poli et al., ICML 2023)

---

## 1. Tóm Tắt Đề Tài (5–7 dòng)

> *Dùng để giải thích nhanh với giảng viên hoặc đưa vào Abstract báo cáo*

Nhóm thực hiện đề tài **khảo sát và tái hiện kiến trúc Hyena Hierarchy**, dựa trên bài báo *"Hyena Hierarchy: Towards Larger Convolutional Language Models"* của Poli et al., được chấp nhận tại ICML 2023. Bài báo giải quyết vấn đề **bottleneck O(L²) của cơ chế Self-Attention** trong Transformer — vốn là rào cản lớn khi xử lý văn bản có ngữ cảnh dài (long sequences). Hyena thay thế Attention bằng một toán tử đệ quy (recurrence) kết hợp **tích chập dài qua FFT** (O(L log L)) và **nhân cổng element-wise**, đạt độ phức tạp tổng thể **O(N·L log L)** — thực sự dưới bậc hai. Thay vì tái hiện toàn bộ bài báo (cần 335M tham số và 825GB dữ liệu), nhóm thực hiện **small-scale reproduction**: train và so sánh Transformer-small và Hyena-small trên dataset WikiText-2, đánh giá perplexity, tốc độ huấn luyện và khả năng xử lý sequence length dài hơn.

---

## 2. Phạm Vi Chính Thức Của Nhóm

### 2.1 Ma trận phạm vi

| Ưu tiên | Hạng mục | Lý do |
|---|---|---|
| 🔴 **Bắt buộc** | Survey lý thuyết Hyena Hierarchy (motivation, kiến trúc, complexity) | Nền tảng của toàn đề tài |
| 🔴 **Bắt buộc** | So sánh Transformer vs Hyena về kiến trúc | Phần lý thuyết trọng tâm |
| 🔴 **Bắt buộc** | Dataset WikiText-2: load, tokenize, dataloader | Cần cho mọi thực nghiệm |
| 🔴 **Bắt buộc** | E1: Train Transformer-small vs Hyena-small, L=256, so sánh PPL | Thực nghiệm cốt lõi |
| 🔴 **Bắt buộc** | Báo cáo PDF hoàn chỉnh | Sản phẩm nộp |
| 🔴 **Bắt buộc** | Slide thuyết trình 10–12 slide | Sản phẩm nộp |
| 🟡 **Nên làm** | E2+E3: Scale sequence length (256→512→1024), đo time/memory | Chứng minh scaling advantage |
| 🟡 **Nên làm** | Loss curves và biểu đồ scaling | Visualize kết quả |
| 🟡 **Nên làm** | GitHub repo có README hướng dẫn chạy | Tính chuyên nghiệp |
| 🟢 **Bonus** | E5: Synthetic recall/copy task | Demo long-context capability |
| 🟢 **Bonus** | E4: Đo GPU memory chi tiết | Nếu có thời gian |
| 🟢 **Bonus** | WikiText-103 subset (10%) | Gần bài gốc hơn |
| ❌ **Không làm** | Train trên The Pile (825GB) | Ngoài tầm tài nguyên |
| ❌ **Không làm** | Model >50M parameters | Không đủ GPU/thời gian |
| ❌ **Không làm** | CUDA kernel custom cho FFT | Quá phức tạp |
| ❌ **Không làm** | Chứng minh toán học đầy đủ Butterfly decomposition | Ngoài phạm vi khóa luận SV |

### 2.2 Tuyên bố phạm vi (dùng trong báo cáo)

> *"Nhóm thực hiện small-scale reproduction nhằm kiểm chứng xu hướng (trend verification) thay vì tái hiện kết quả số tuyệt đối. Mục tiêu là quan sát: (1) chất lượng ngôn ngữ (perplexity) tương đương giữa Transformer và Hyena ở scale nhỏ; (2) Hyena có lợi thế rõ về tốc độ và bộ nhớ khi sequence length tăng."*

---

## 3. Phân Công Task Cho 3 Thành Viên

---

### 👤 Thành Viên 1 — Lý Thuyết & Paper Survey

**Vai trò:** Chuyên gia lý thuyết và viết báo cáo phần lý luận

#### Nhiệm vụ chi tiết

| # | Task | Chi tiết | Deadline |
|---|---|---|---|
| T1.1 | Đọc và tóm tắt toàn bộ bài báo Hyena | Abstract → Conclusion, ghi chú theo từng section | Cuối Tuần 1 |
| T1.2 | Viết `paper_summary.md` | Motivation, problem, contribution, kết quả bài gốc | Cuối Tuần 1 |
| T1.3 | Nghiên cứu Transformer/Self-Attention | Q,K,V, scaled dot-product, causal mask, MHA | Cuối Tuần 1 |
| T1.4 | Viết `theory_attention.md` | Công thức, sơ đồ, phân tích O(L²) | Cuối Tuần 1 |
| T1.5 | Tạo bảng so sánh Transformer vs Hyena | Kiến trúc, complexity, parameters, context | Cuối Tuần 1 |
| T1.6 | Nghiên cứu landscape alternatives | SSM (S4), H3, Mamba, RWKV — vị trí của Hyena | Đầu Tuần 2 |
| T1.7 | Viết báo cáo Sections 1, 2, 3 | Giới thiệu, Cơ sở lý thuyết, Bài báo Hyena | Tuần 2–3 |
| T1.8 | Chuẩn bị speaker notes cho slide 1–5 | Nội dung, giải thích, câu hỏi dự đoán | Tuần 3 |
| T1.9 | Tổng hợp phần Thảo luận (Section 8) | Ưu/nhược, giới hạn, hướng tương lai | Tuần 3 |

#### File cần tạo

```
docs/
├── paper_summary.md          # Tóm tắt bài báo theo từng section
├── theory_attention.md       # Lý thuyết Transformer + Attention
├── comparison_table.md       # Bảng so sánh Transformer vs Hyena
└── related_work_notes.md     # Ghi chú SSM, S4, H3, Mamba
```

#### Rủi ro cần lưu ý
- **Toán học nặng (FFT, butterfly):** Không cần chứng minh đầy đủ. Hiểu ở mức "tại sao O(L log L)" là đủ
- **Quá nhiều bài liên quan:** Chỉ cần nắm rõ: H3, S4, và so sánh với Transformer. Mamba đề cập ngắn như hướng tương lai
- **Thời gian viết báo cáo:** Ưu tiên hoàn thành Section 1, 2, 3 trước Tuần 3

#### Phối hợp với 2 thành viên còn lại
- → **TV2:** Cung cấp thống kê dataset để viết Section 5
- → **TV3:** Nhận bảng kết quả thực nghiệm để viết Section 7, 8
- → **Cả nhóm:** Review chéo nội dung báo cáo cuối Tuần 3

---

### 👤 Thành Viên 2 — Dataset & Experiment Pipeline

**Vai trò:** Data engineer và quản lý infrastructure thực nghiệm

#### Nhiệm vụ chi tiết

| # | Task | Chi tiết | Deadline |
|---|---|---|---|
| T2.1 | Tạo GitHub repo và cấu trúc thư mục | Clone template, tạo `README.md` ban đầu, `.gitignore` | Ngày 1–2 Tuần 1 |
| T2.2 | Load WikiText-2 từ HuggingFace | `datasets.load_dataset("wikitext", "wikitext-2-raw-v1")` | Giữa Tuần 1 |
| T2.3 | Khám phá dataset | Đếm tokens, phân tích văn bản, thống kê độ dài | Giữa Tuần 1 |
| T2.4 | Tokenization | Dùng GPT-2 tokenizer (BPE), encode toàn bộ dataset | Giữa Tuần 1 |
| T2.5 | Tạo dataloader | Sliding window chunking theo `seq_len`, batch, padding | Cuối Tuần 1 |
| T2.6 | Viết `data/preprocess.py` | Script tái sử dụng được, có argparse cho seq_len | Cuối Tuần 1 |
| T2.7 | Viết `notebooks/01_data_exploration.ipynb` | Load → tokenize → visualize → thống kê | Cuối Tuần 1 |
| T2.8 | Chuẩn bị synthetic recall task (optional) | Tạo generator cho associative recall dataset | Tuần 2 |
| T2.9 | Setup logging framework | Cấu hình TensorBoard hoặc simple CSV logger | Đầu Tuần 2 |
| T2.10 | Hỗ trợ TV3 debug dataloader | Đảm bảo data pipeline tương thích với training loop | Tuần 2 |
| T2.11 | Viết `README.md` hoàn chỉnh | Hướng dẫn setup, chạy dataset, chạy training | Tuần 3 |
| T2.12 | Chuẩn bị nội dung báo cáo Section 5 | Dataset, tiền xử lý, thống kê | Tuần 3 |

#### File cần tạo

```
data/
├── preprocess.py             # Script tokenize + tạo dataloader
└── synthetic_task.py         # (Bonus) Associative recall generator

notebooks/
├── 01_data_exploration.ipynb # Khám phá dataset
└── 02_synthetic_task.ipynb   # (Bonus) Demo synthetic task

README.md                     # Hướng dẫn đầy đủ
requirements.txt              # Danh sách dependencies
.gitignore                    # Bỏ qua .pyc, checkpoints, data lớn
```

#### Template `data/preprocess.py`

```python
"""
preprocess.py — WikiText-2 Data Pipeline
Usage: python data/preprocess.py --seq_len 256 --split train
"""
import argparse
from datasets import load_dataset
from transformers import GPT2Tokenizer
import torch
from torch.utils.data import Dataset, DataLoader

def load_wikitext2(split="train"):
    dataset = load_dataset("wikitext", "wikitext-2-raw-v1", split=split)
    return dataset

def tokenize(dataset, tokenizer):
    text = "\n".join(dataset["text"])
    tokens = tokenizer.encode(text)
    return torch.tensor(tokens, dtype=torch.long)

class SequenceDataset(Dataset):
    def __init__(self, tokens, seq_len):
        self.tokens = tokens
        self.seq_len = seq_len
        self.n = len(tokens) // seq_len

    def __len__(self):
        return self.n

    def __getitem__(self, idx):
        start = idx * self.seq_len
        x = self.tokens[start : start + self.seq_len]
        y = self.tokens[start + 1 : start + self.seq_len + 1]
        return x, y

def get_dataloader(split="train", seq_len=256, batch_size=16):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    dataset = load_wikitext2(split)
    tokens = tokenize(dataset, tokenizer)
    seq_dataset = SequenceDataset(tokens, seq_len)
    return DataLoader(seq_dataset, batch_size=batch_size, shuffle=(split=="train"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seq_len", type=int, default=256)
    parser.add_argument("--split", type=str, default="train")
    args = parser.parse_args()
    loader = get_dataloader(split=args.split, seq_len=args.seq_len)
    print(f"[{args.split}] {len(loader)} batches, seq_len={args.seq_len}")
```

#### Rủi ro cần lưu ý
- **GPT-2 tokenizer download chậm:** Cache lại sau lần đầu; dùng `tokenizer.save_pretrained("./tokenizer")` để offline
- **Dataloader không khớp với model:** Luôn kiểm tra `x.shape`, `y.shape` trước khi giao cho TV3
- **OOM khi seq_len lớn:** Giảm `batch_size` khi tăng `seq_len`

#### Phối hợp với 2 thành viên còn lại
- → **TV1:** Cung cấp thống kê dataset (số token, vocabulary) để viết Section 5
- → **TV3:** Giao `get_dataloader()` function hoàn chỉnh, test cùng nhau trên notebook
- → **Cả nhóm:** Đảm bảo repo có thể clone và chạy ngay từ README

---

### 👤 Thành Viên 3 — Model, Training & Evaluation

**Vai trò:** ML engineer, chạy thực nghiệm và tổng hợp kết quả

#### Nhiệm vụ chi tiết

| # | Task | Chi tiết | Deadline |
|---|---|---|---|
| T3.1 | Implement `models/transformer.py` | GPT-like: Embedding, CausalSelfAttention, Block, LM | Đầu Tuần 2 |
| T3.2 | Implement `models/hyena.py` | HyenaFilter + HyenaOperator + HyenaLM | Giữa Tuần 2 |
| T3.3 | Viết `train.py` | Training loop, AdamW, LR scheduler, checkpoint | Giữa Tuần 2 |
| T3.4 | Viết `evaluate.py` | Validation loss, perplexity, time measurement | Giữa Tuần 2 |
| T3.5 | Chạy E1: Baseline comparison | Transformer vs Hyena, WikiText-2, L=256 | Cuối Tuần 2 |
| T3.6 | Debug và fix issues | Numerical instability, convergence, OOM | Tuần 2 |
| T3.7 | Chạy E2+E3: Scale seq length | L=256→512→1024, đo time/memory | Đầu Tuần 3 |
| T3.8 | Xuất kết quả ra CSV | `results/experiment_results.csv` | Đầu Tuần 3 |
| T3.9 | Vẽ biểu đồ | Loss curves, time/memory vs L, PPL comparison | Giữa Tuần 3 |
| T3.10 | Viết `notebooks/02_model_training.ipynb` | Walkthrough training trên Colab | Giữa Tuần 3 |
| T3.11 | Chuẩn bị nội dung báo cáo Section 6, 7 | Thiết lập thực nghiệm, kết quả | Tuần 3 |
| T3.12 | (Bonus) E5: Synthetic recall | Train cả hai model, đo accuracy | Nếu còn thời gian |

#### File cần tạo

```
models/
├── transformer.py            # Transformer-small (GPT-like)
└── hyena.py                  # Hyena-small

train.py                      # Training loop chính
evaluate.py                   # Evaluation script

results/
├── E1_baseline.csv           # PPL Transformer vs Hyena, L=256
├── E2_transformer_scale.csv  # Time/Memory Transformer vs L
├── E3_hyena_scale.csv        # Time/Memory Hyena vs L
└── plots/
    ├── loss_curves.png
    ├── scaling_time.png
    └── scaling_memory.png

notebooks/
├── 02_model_training.ipynb   # Training walkthrough
└── 03_results_analysis.ipynb # Phân tích kết quả
```

#### Template `models/transformer.py`

```python
"""
transformer.py — GPT-like Transformer (small scale)
Config: 4 layers, 4 heads, d_model=256, d_ff=1024
"""
import torch
import torch.nn as nn
import math

class CausalSelfAttention(nn.Module):
    def __init__(self, d_model, n_heads, max_seq_len, dropout=0.1):
        super().__init__()
        assert d_model % n_heads == 0
        self.n_heads = n_heads
        self.d_head = d_model // n_heads
        self.qkv = nn.Linear(d_model, 3 * d_model)
        self.proj = nn.Linear(d_model, d_model)
        self.dropout = nn.Dropout(dropout)
        # Causal mask
        mask = torch.tril(torch.ones(max_seq_len, max_seq_len))
        self.register_buffer("mask", mask.unsqueeze(0).unsqueeze(0))

    def forward(self, x):
        B, L, D = x.shape
        q, k, v = self.qkv(x).split(D, dim=-1)
        q = q.view(B, L, self.n_heads, self.d_head).transpose(1, 2)
        k = k.view(B, L, self.n_heads, self.d_head).transpose(1, 2)
        v = v.view(B, L, self.n_heads, self.d_head).transpose(1, 2)
        scale = math.sqrt(self.d_head)
        attn = (q @ k.transpose(-2, -1)) / scale
        attn = attn.masked_fill(self.mask[:, :, :L, :L] == 0, float("-inf"))
        attn = torch.softmax(attn, dim=-1)
        attn = self.dropout(attn)
        out = (attn @ v).transpose(1, 2).contiguous().view(B, L, D)
        return self.proj(out)

class TransformerBlock(nn.Module):
    def __init__(self, d_model, n_heads, d_ff, max_seq_len, dropout=0.1):
        super().__init__()
        self.ln1 = nn.LayerNorm(d_model)
        self.attn = CausalSelfAttention(d_model, n_heads, max_seq_len, dropout)
        self.ln2 = nn.LayerNorm(d_model)
        self.ff = nn.Sequential(
            nn.Linear(d_model, d_ff), nn.GELU(),
            nn.Linear(d_ff, d_model), nn.Dropout(dropout)
        )

    def forward(self, x):
        x = x + self.attn(self.ln1(x))
        x = x + self.ff(self.ln2(x))
        return x

class TransformerLM(nn.Module):
    def __init__(self, vocab_size, d_model=256, n_layers=4, n_heads=4,
                 d_ff=1024, max_seq_len=1024, dropout=0.1):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, d_model)
        self.pos_embed = nn.Embedding(max_seq_len, d_model)
        self.blocks = nn.ModuleList([
            TransformerBlock(d_model, n_heads, d_ff, max_seq_len, dropout)
            for _ in range(n_layers)
        ])
        self.ln_f = nn.LayerNorm(d_model)
        self.lm_head = nn.Linear(d_model, vocab_size, bias=False)

    def forward(self, x):
        B, L = x.shape
        pos = torch.arange(L, device=x.device)
        h = self.embed(x) + self.pos_embed(pos)
        for block in self.blocks:
            h = block(h)
        h = self.ln_f(h)
        return self.lm_head(h)
```

#### Template `models/hyena.py`

```python
"""
hyena.py — Hyena-small (order N=2, implicit FFT filter)
Simplified pure-Python implementation (no CUDA kernels required)
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class HyenaFilter(nn.Module):
    """Implicit long convolution filter via FFN + positional encoding"""
    def __init__(self, d_model, order=2, filter_dim=64, max_seq_len=1024):
        super().__init__()
        self.order = order
        self.d_model = d_model
        self.max_seq_len = max_seq_len
        # Positional encoding dimension
        self.pos_emb_dim = filter_dim
        # FFN: pos → filter values for all orders
        self.ffn = nn.Sequential(
            nn.Linear(filter_dim, filter_dim), nn.SiLU(),
            nn.Linear(filter_dim, order * d_model)
        )
        # Learnable decay window
        self.log_decay = nn.Parameter(torch.zeros(order, d_model))

    def _positional_encoding(self, L, device):
        t = torch.linspace(0, 1, L, device=device).unsqueeze(-1)
        freqs = torch.exp(
            torch.linspace(0, math.log(1e4), self.pos_emb_dim // 2, device=device)
        )
        pos = torch.cat([torch.sin(t * freqs), torch.cos(t * freqs)], dim=-1)
        return pos  # (L, filter_dim)

    def forward(self, L):
        device = self.log_decay.device
        t_pos = self._positional_encoding(L, device)  # (L, filter_dim)
        h = self.ffn(t_pos)                           # (L, order * d_model)
        h = h.view(L, self.order, self.d_model)       # (L, order, d_model)
        # Apply exponential decay window
        t = torch.linspace(0, 1, L, device=device)
        decay = torch.exp(-torch.exp(self.log_decay) * t.view(-1, 1, 1))
        h = h * decay
        return h.permute(1, 2, 0)  # (order, d_model, L)

class HyenaOperator(nn.Module):
    """Hyena recurrence: z^(n+1) = x^n · FFTConv(h^n, z^n)"""
    def __init__(self, d_model, order=2, filter_dim=64, max_seq_len=1024, dropout=0.1):
        super().__init__()
        self.order = order
        self.d_model = d_model
        # Input projection: u → (order+1) * d_model (x^1,...,x^N, v)
        self.input_proj = nn.Linear(d_model, (order + 1) * d_model)
        self.filter = HyenaFilter(d_model, order, filter_dim, max_seq_len)
        self.out_proj = nn.Linear(d_model, d_model)
        self.dropout = nn.Dropout(dropout)

    def _fft_conv(self, h, v):
        """Causal convolution via FFT: O(L log L)"""
        L = v.shape[-1]
        fft_size = 2 * L  # Zero-pad for linear (causal) convolution
        H = torch.fft.rfft(h, n=fft_size)
        V = torch.fft.rfft(v, n=fft_size)
        Y = H * V
        y = torch.fft.irfft(Y, n=fft_size)[..., :L]
        return y

    def forward(self, u):
        B, L, D = u.shape
        # Project input to (order+1) gates
        z_all = self.input_proj(u)  # (B, L, (N+1)*D)
        z_all = z_all.view(B, L, self.order + 1, D)
        z_all = z_all.permute(2, 0, 3, 1)  # (N+1, B, D, L)
        # Get implicit filters
        h_all = self.filter(L)  # (order, D, L)
        # Hyena recurrence
        z = z_all[-1]  # v: (B, D, L)
        for n in range(self.order - 1, -1, -1):
            h = h_all[n]                    # (D, L)
            x = z_all[n]                    # (B, D, L)
            conv = self._fft_conv(h, z)     # (B, D, L)
            z = x * conv                    # element-wise gating
        y = z.permute(0, 2, 1)             # (B, L, D)
        return self.dropout(self.out_proj(y))

class HyenaBlock(nn.Module):
    def __init__(self, d_model, order=2, filter_dim=64, d_ff=1024,
                 max_seq_len=1024, dropout=0.1):
        super().__init__()
        self.ln1 = nn.LayerNorm(d_model)
        self.hyena = HyenaOperator(d_model, order, filter_dim, max_seq_len, dropout)
        self.ln2 = nn.LayerNorm(d_model)
        self.ff = nn.Sequential(
            nn.Linear(d_model, d_ff), nn.GELU(),
            nn.Linear(d_ff, d_model), nn.Dropout(dropout)
        )

    def forward(self, x):
        x = x + self.hyena(self.ln1(x))
        x = x + self.ff(self.ln2(x))
        return x

class HyenaLM(nn.Module):
    def __init__(self, vocab_size, d_model=256, n_layers=4, order=2,
                 filter_dim=64, d_ff=1024, max_seq_len=1024, dropout=0.1):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, d_model)
        self.pos_embed = nn.Embedding(max_seq_len, d_model)
        self.blocks = nn.ModuleList([
            HyenaBlock(d_model, order, filter_dim, d_ff, max_seq_len, dropout)
            for _ in range(n_layers)
        ])
        self.ln_f = nn.LayerNorm(d_model)
        self.lm_head = nn.Linear(d_model, vocab_size, bias=False)

    def forward(self, x):
        B, L = x.shape
        pos = torch.arange(L, device=x.device)
        h = self.embed(x) + self.pos_embed(pos)
        for block in self.blocks:
            h = block(h)
        h = self.ln_f(h)
        return self.lm_head(h)
```

#### Rủi ro cần lưu ý
- **FFT numerical instability:** Kiểm tra NaN/Inf sau mỗi bước. Thêm `torch.nan_to_num()` nếu cần
- **Hyena converge chậm:** Dùng LR nhỏ hơn (1e-4 thay vì 1e-3) và warmup nhiều hơn
- **OOM ở L=1024:** Giảm `batch_size=4` hoặc `d_model=128`
- **Kết quả PPL không bằng Transformer:** Bình thường ở scale nhỏ — cần giải thích trong báo cáo

#### Phối hợp với 2 thành viên còn lại
- → **TV2:** Nhận `get_dataloader()` để tích hợp vào `train.py`
- → **TV1:** Giao bảng kết quả CSV + biểu đồ để viết Section 7, 8
- → **Cả nhóm:** Demo chạy trên Colab trước buổi nộp

---

## 4. Timeline Triển Khai 3 Tuần

### 🗓️ TUẦN 1 — Hiểu Bài Báo, Chốt Scope, Chuẩn Bị Dataset

**Mục tiêu cuối tuần:**
- Mọi thành viên đã đọc qua bài báo ít nhất 1 lần
- Dataset WikiText-2 load và tokenize được
- GitHub repo có cấu trúc ban đầu
- Phân công rõ ràng, không chồng chéo

| Ngày | Công việc | Người | Output | ✅ |
|---|---|---|---|---|
| Ngày 1 | Tạo GitHub repo, cài môi trường | TV2 | Repo + `requirements.txt` | ☐ |
| Ngày 1–2 | Đọc Abstract, Introduction, Section 1 bài báo | Cả nhóm | Ghi chú cá nhân | ☐ |
| Ngày 2–3 | Đọc Section 2 (Preliminaries), 3 (Hyena Operator) | TV1 + TV3 | Mind map + sơ đồ | ☐ |
| Ngày 2–3 | Load WikiText-2, khám phá dataset | TV2 | Notebook + thống kê | ☐ |
| Ngày 3–4 | Viết `paper_summary.md`, `theory_attention.md` | TV1 | 2 file docs | ☐ |
| Ngày 3–4 | Tokenize + tạo dataloader cơ bản | TV2 | `preprocess.py` v1 | ☐ |
| Ngày 4–5 | Đọc Section 4 (Experiments) + Related Work | TV1 | Bảng so sánh + kết quả gốc | ☐ |
| Ngày 5–6 | Tìm hiểu PyTorch: Embedding, Linear, FFT | TV3 | Proof-of-concept FFT conv | ☐ |
| Ngày 6–7 | Họp nhóm: chốt scope, phân công chi tiết | Cả nhóm | Scope document | ☐ |
| Cuối Tuần 1 | Commit: docs/, data/, README sơ bộ | TV2 | Repo cập nhật | ☐ |

**Checklist cuối Tuần 1:**
- [ ] `paper_summary.md` hoàn thành (TV1)
- [ ] `theory_attention.md` hoàn thành (TV1)
- [ ] WikiText-2 load được, thống kê cơ bản (TV2)
- [ ] `data/preprocess.py` chạy được (TV2)
- [ ] `notebooks/01_data_exploration.ipynb` hoàn thành (TV2)
- [ ] FFT convolution demo nhỏ chạy được (TV3)
- [ ] GitHub repo có cấu trúc đầy đủ (TV2)
- [ ] Họp nhóm và chốt scope (Cả nhóm)

---

### 🗓️ TUẦN 2 — Cài Model và Chạy Thực Nghiệm Cơ Bản

**Mục tiêu cuối tuần:**
- Transformer-small chạy được, loss giảm
- Hyena-small chạy được, không có lỗi
- Có kết quả E1 sơ bộ (dù chưa tối ưu)

| Ngày | Công việc | Người | Output | ✅ |
|---|---|---|---|---|
| Ngày 8–9 | Implement `models/transformer.py` | TV3 | Transformer chạy được | ☐ |
| Ngày 8–9 | Nghiên cứu landscape: S4, H3, Mamba | TV1 | `related_work_notes.md` | ☐ |
| Ngày 8–9 | Hoàn thiện `preprocess.py`, test với TV3 | TV2 | Dataloader verified | ☐ |
| Ngày 10–11 | Implement `models/hyena.py` (simplified) | TV3 | Hyena chạy được (no error) | ☐ |
| Ngày 10–11 | Implement `train.py` | TV3 | Training loop hoàn chỉnh | ☐ |
| Ngày 10–11 | Cài synthetic task generator (bonus) | TV2 | `data/synthetic_task.py` | ☐ |
| Ngày 11–12 | Debug training: NaN, OOM, convergence | TV3 + TV2 | Model converge được | ☐ |
| Ngày 12–13 | Chạy E1: Transformer L=256, 20 epochs | TV3 | `results/E1_transformer.csv` | ☐ |
| Ngày 12–13 | Chạy E1: Hyena L=256, 20 epochs | TV3 | `results/E1_hyena.csv` | ☐ |
| Ngày 13–14 | Implement `evaluate.py` + đo PPL | TV3 | Perplexity cho cả 2 model | ☐ |
| Ngày 13–14 | Bắt đầu viết báo cáo Section 1, 2 | TV1 | Draft Sections 1–2 | ☐ |
| Cuối Tuần 2 | Họp nhóm: review kết quả E1, điều chỉnh plan | Cả nhóm | Updated plan | ☐ |

**Checklist cuối Tuần 2:**
- [ ] `models/transformer.py` chạy, loss giảm (TV3)
- [ ] `models/hyena.py` chạy, không lỗi (TV3)
- [ ] `train.py` hoàn chỉnh (TV3)
- [ ] `evaluate.py` tính đúng perplexity (TV3)
- [ ] Có kết quả E1 dù chưa tối ưu (TV3)
- [ ] Draft Section 1, 2 báo cáo (TV1)
- [ ] Dataloader tương thích training loop (TV2)

---

### 🗓️ TUẦN 3 — Hoàn Thiện Kết Quả, Báo Cáo và Slide

**Mục tiêu cuối tuần:**
- Tất cả thực nghiệm hoàn thành
- Báo cáo PDF hoàn chỉnh
- Slide thuyết trình sẵn sàng
- Code có thể chạy lại từ README

| Ngày | Công việc | Người | Output | ✅ |
|---|---|---|---|---|
| Ngày 15–16 | Chạy E2+E3: Scale L=512, 1024 | TV3 | 4 CSV files (E2, E3) | ☐ |
| Ngày 15–16 | Viết báo cáo Section 3 (Hyena Hierarchy) | TV1 | Draft Section 3 | ☐ |
| Ngày 15–16 | Hoàn thiện `README.md` | TV2 | README đầy đủ | ☐ |
| Ngày 17 | Vẽ biểu đồ: loss curves, scaling time/memory | TV3 | PNG files trong `results/plots/` | ☐ |
| Ngày 17 | Viết báo cáo Section 4, 5 | TV1 + TV2 | Draft Sections 4–5 | ☐ |
| Ngày 17–18 | Viết báo cáo Section 6, 7, 8 | TV1 + TV3 | Draft Sections 6–8 | ☐ |
| Ngày 18 | (Bonus) Chạy E5: Synthetic recall | TV3 | Accuracy table | ☐ |
| Ngày 18–19 | Làm slide 1–6 | TV1 | Slides 1–6 | ☐ |
| Ngày 18–19 | Làm slide 7–12 | TV2 + TV3 | Slides 7–12 | ☐ |
| Ngày 19 | Review chéo báo cáo | Cả nhóm | Báo cáo reviewed | ☐ |
| Ngày 20 | Finalize báo cáo PDF | TV1 | `report/report.pdf` | ☐ |
| Ngày 20 | Finalize slide PDF/PPTX | TV2 | `slides/presentation.pdf` | ☐ |
| Ngày 21 | Clean up repo, final commit | TV2 | Repo public + tagged | ☐ |
| Ngày 21 | Rehearsal thuyết trình | Cả nhóm | Sẵn sàng trình bày | ☐ |

**Checklist cuối Tuần 3 (Submit checklist):**
- [ ] Kết quả E1 đầy đủ và chính xác
- [ ] Kết quả E2+E3 đầy đủ
- [ ] Biểu đồ loss curves, scaling rõ ràng
- [ ] Báo cáo PDF ≥15 trang, đầy đủ 10 sections
- [ ] Slide 10–12 slide, có speaker notes
- [ ] `README.md` đủ để chạy lại code
- [ ] Repo clean, không có file rác
- [ ] Đã rehearsal ít nhất 1 lần

---

## 5. Checklist Kỹ Thuật

### 5.1 Checklist theo thành viên

#### TV2 — Environment & Data
- [ ] `python --version` ≥ 3.9
- [ ] `pip install torch transformers datasets` thành công
- [ ] `import torch; torch.cuda.is_available()` trả về `True` trên Colab
- [ ] `load_dataset("wikitext", "wikitext-2-raw-v1")` hoạt động
- [ ] GPT-2 tokenizer encode/decode bình thường
- [ ] `SequenceDataset.__getitem__` trả đúng `(x, y)` shape `(seq_len,)`
- [ ] `DataLoader` batch đúng: shape `(batch_size, seq_len)`
- [ ] Train/val/test split độc lập
- [ ] `requirements.txt` chạy được trên môi trường sạch

#### TV3 — Models & Training
- [ ] `TransformerLM(vocab_size=50257).forward(x)` không lỗi, output shape `(B, L, V)`
- [ ] `HyenaLM(vocab_size=50257).forward(x)` không lỗi, output shape `(B, L, V)`
- [ ] Loss sau epoch 1: Transformer < 10.0 (giảm so với random = ln(V) ≈ 10.8)
- [ ] Loss Hyena giảm theo epoch (không nan, không inf)
- [ ] `evaluate.py` tính đúng: `perplexity = exp(val_loss)`
- [ ] Training time per step được log ra
- [ ] GPU memory được đo (nếu có GPU)
- [ ] Checkpoint lưu và load được
- [ ] `results/E1_baseline.csv` có đầy đủ cột: epoch, train_loss, val_loss, ppl, time_s
- [ ] Biểu đồ có đúng title, axis label, legend

#### TV1 — Documentation
- [ ] `paper_summary.md` cover đủ: motivation, method, results
- [ ] `theory_attention.md` giải thích được O(L²) bằng ví dụ số
- [ ] Bảng so sánh Transformer vs Hyena có ≥5 tiêu chí
- [ ] Báo cáo có đủ 10 sections
- [ ] Tài liệu tham khảo đúng format (IEEE hoặc APA)
- [ ] Biểu đồ/bảng từ bài báo gốc được cite đúng nguồn

### 5.2 Checklist `requirements.txt` tham khảo

```txt
torch>=2.0.0
transformers>=4.30.0
datasets>=2.12.0
numpy>=1.24.0
matplotlib>=3.7.0
pandas>=2.0.0
jupyter>=1.0.0
tqdm>=4.65.0
```

---

## 6. Cấu Trúc GitHub Repo

```
hyena-reproduction/
│
├── README.md                        # [TV2] Tuần 1-3 | Hướng dẫn setup + chạy
├── requirements.txt                 # [TV2] Tuần 1   | Dependencies
├── .gitignore                       # [TV2] Tuần 1   | Bỏ qua .pyc, *.pt, data/
│
├── data/
│   ├── preprocess.py                # [TV2] Tuần 1   | Load + tokenize + dataloader
│   └── synthetic_task.py            # [TV2] Tuần 2   | (Bonus) Recall task generator
│
├── models/
│   ├── __init__.py                  # [TV3] Tuần 2   | Export TransformerLM, HyenaLM
│   ├── transformer.py               # [TV3] Tuần 2   | GPT-like Transformer-small
│   └── hyena.py                     # [TV3] Tuần 2   | Hyena-small (simplified)
│
├── train.py                         # [TV3] Tuần 2   | Training loop chính
├── evaluate.py                      # [TV3] Tuần 2   | Validation + metrics
│
├── notebooks/
│   ├── 01_data_exploration.ipynb    # [TV2] Tuần 1   | Dataset analysis
│   ├── 02_model_training.ipynb      # [TV3] Tuần 3   | Training walkthrough (Colab)
│   └── 03_results_analysis.ipynb    # [TV3] Tuần 3   | Plots + analysis
│
├── results/
│   ├── E1_baseline.csv              # [TV3] Tuần 2   | PPL Transformer vs Hyena L=256
│   ├── E2_transformer_scale.csv     # [TV3] Tuần 3   | Transformer time/mem vs L
│   ├── E3_hyena_scale.csv           # [TV3] Tuần 3   | Hyena time/mem vs L
│   └── plots/
│       ├── loss_curves.png          # [TV3] Tuần 3   | Train/val loss per epoch
│       ├── scaling_time.png         # [TV3] Tuần 3   | Time vs L: Transformer vs Hyena
│       └── scaling_memory.png       # [TV3] Tuần 3   | Memory vs L
│
├── docs/
│   ├── paper_summary.md             # [TV1] Tuần 1   | Tóm tắt bài báo Hyena
│   ├── theory_attention.md          # [TV1] Tuần 1   | Lý thuyết Transformer
│   ├── comparison_table.md          # [TV1] Tuần 1   | So sánh Transformer vs Hyena
│   └── related_work_notes.md        # [TV1] Tuần 2   | SSM, H3, Mamba
│
├── report/
│   └── report.pdf                   # [TV1] Tuần 3   | Báo cáo PDF cuối cùng
│
└── slides/
    └── presentation.pdf             # [Cả nhóm] Tuần 3 | Slide thuyết trình
```

---

## 7. Bảng Thí Nghiệm Theo Mức Độ Ưu Tiên

### 🔴 Must-have

| Exp | Tên | Dataset | Model | Seq Length | Metric | Kết quả kỳ vọng | Phụ trách | Bắt buộc |
|---|---|---|---|---|---|---|---|---|
| **E1** | Baseline comparison | WikiText-2 | Transformer-small vs Hyena-small | 256 | Train loss, Val loss, PPL, Training time/step | PPL ngang nhau ±15%; loss giảm đều | TV3 | ✅ Có |

### 🟡 Should-have

| Exp | Tên | Dataset | Model | Seq Length | Metric | Kết quả kỳ vọng | Phụ trách | Bắt buộc |
|---|---|---|---|---|---|---|---|---|
| **E2** | Scale seq (Transformer) | WikiText-2 | Transformer-small | 256→512→1024 | Time/step (s), GPU mem (MB) | Time tăng ~4x khi L tăng 2x | TV3 | ⚠️ Nên |
| **E3** | Scale seq (Hyena) | WikiText-2 | Hyena-small | 256→512→1024→2048 | Time/step (s), GPU mem (MB) | Time tăng ~2x khi L tăng 2x | TV3 | ⚠️ Nên |

### 🟢 Nice-to-have

| Exp | Tên | Dataset | Model | Seq Length | Metric | Kết quả kỳ vọng | Phụ trách | Bắt buộc |
|---|---|---|---|---|---|---|---|---|
| **E4** | Memory comparison | WikiText-2 | Transformer vs Hyena | 256, 512, 1024 | Peak GPU memory (MB) | Hyena < Transformer ở L lớn | TV3 | ❌ Bonus |
| **E5** | Synthetic recall | Synthetic | Transformer vs Hyena | 128, 256, 512 | Accuracy (%) | Hyena ≥ Transformer | TV2+TV3 | ❌ Bonus |

---

## 8. Skeleton Báo Cáo Đầy Đủ

| # | Tên mục | Nội dung cần viết | Số trang | Hình/Bảng | Phụ trách |
|---|---|---|---|---|---|
| **1** | **Giới thiệu** | Bối cảnh NLP; vấn đề O(L²); mục tiêu đề tài; đóng góp nhóm; cấu trúc báo cáo | 1.5–2 | Biểu đồ complexity O(L²) vs O(L log L) | TV1 |
| **2** | **Cơ Sở Lý Thuyết** | 2.1 LM autoregressive + perplexity; 2.2 Transformer + MHA; 2.3 Causal masking; 2.4 Convolution + FFT; 2.5 SSM sơ lược; 2.6 Landscape (H3, Mamba) | 4–5 | Sơ đồ Transformer block; công thức Attention; bảng so sánh landscape | TV1 |
| **3** | **Bài Báo Hyena Hierarchy** | 3.1 Motivation; 3.2 Hyena operator + công thức; 3.3 Implicit filter FFN; 3.4 Matrix decomposition (mức tổng quan); 3.5 Complexity analysis; 3.6 Kết quả bài gốc (WT103, The Pile) | 3–4 | Figure 1 bài báo (recurrence); Figure 3 (filter); bảng kết quả gốc | TV1 |
| **4** | **Phương Pháp Tái Hiện** | 4.1 Lý do chọn small-scale; 4.2 Config Transformer-small; 4.3 Config Hyena-small; 4.4 Khác biệt vs bài gốc; 4.5 Mong đợi về kết quả | 1.5–2 | Bảng config 2 model; sơ đồ kiến trúc Hyena-small | TV1 + TV3 |
| **5** | **Dataset và Tiền Xử Lý** | 5.1 WikiText-2 + nguồn; 5.2 Thống kê (tokens, vocab, avg length); 5.3 Tokenization BPE; 5.4 Sliding window pipeline; 5.5 (Bonus) Synthetic task | 1.5–2 | Bảng thống kê dataset; sơ đồ pipeline | TV2 |
| **6** | **Thiết Lập Thực Nghiệm** | 6.1 Môi trường (Python, PyTorch, GPU); 6.2 Hyperparameters; 6.3 Metrics; 6.4 Bảng mô tả E1–E3(–E5) | 1–1.5 | Bảng hyperparameters; bảng E1–E5 | TV3 |
| **7** | **Kết Quả và Đánh Giá** | 7.1 E1: loss curves + PPL table; 7.2 E2+E3: bảng time/memory; 7.3 So sánh scaling; 7.4 (Bonus) E5 accuracy | 2.5–3 | Loss curves plot; scaling chart; PPL table | TV3 + TV1 |
| **8** | **Thảo Luận** | 8.1 Ưu điểm Hyena; 8.2 Nhược điểm; 8.3 Giới hạn reproduction; 8.4 Hướng tương lai (Mamba, RWKV) | 1.5–2 | Bảng ưu/nhược điểm | TV1 |
| **9** | **Kết Luận** | Tóm tắt đóng góp; nhận xét tổng quát về Hyena; hướng phát triển | 0.5 | — | TV1 |
| **10** | **Tài Liệu Tham Khảo** | ≥8 references, đúng format IEEE/APA | 1 | — | TV1 |

**Tổng cộng: ≈ 18–23 trang** (không tính cover, mục lục, phụ lục)

---

## 9. Skeleton Slide (12 Slide)

| # | Tiêu đề | Bullet chính | Hình/Bảng | Speaker Note | Phụ trách |
|---|---|---|---|---|---|
| **1** | Tên đề tài & Nhóm | Tên đề tài đầy đủ; Tên 3 thành viên; Môn học + Ngày | Logo trường | "Chào thầy/cô và các bạn, nhóm em hôm nay trình bày về đề tài..." | Cả nhóm |
| **2** | Động lực (Motivation) | Transformer thống trị NLP; O(L²) là bottleneck; Ví dụ: L=64K → OOM; Cần giải pháp subquadratic | Biểu đồ O(L²) vs O(L log L) | "Kể từ năm 2017, Transformer gần như là lựa chọn mặc định... nhưng khi sequence dài, attention matrix bùng nổ..." | TV1 |
| **3** | Self-Attention Recap | `Attention = softmax(QKᵀ/√d)·V`; Ma trận L×L; 3 đặc tính (data-controlled, sublinear params, unrestricted context) | Sơ đồ attention matrix hình vuông L×L | "Attention rất mạnh vì nó phụ thuộc vào dữ liệu... nhưng chính sự linh hoạt đó khiến nó tốn O(L²)..." | TV1 |
| **4** | Landscape: Alternatives to Attention | Timeline: S4→H3→**Hyena**→Mamba; Phân loại: SSM / Attention / Hybrid | Timeline diagram | "Nhiều hướng đã được thử... nhóm tập trung vào Hyena vì là bước đột phá trước Mamba" | TV1 |
| **5** | Hyena Hierarchy — Core Idea | `z^(n+1) = x^n · FFTConv(h^n, z^n)`; 2 nguyên thủy: Long conv + Gating; O(N·L log L) | Sơ đồ recurrence (Figure 1 bài báo) | "Đây là slide quan trọng nhất. Hyena chỉ cần 2 phép tính đơn giản..." | TV1 |
| **6** | Implicit Long Filter | `h_t = Window(t) · FFN(PosEnc(t))`; Tại sao implicit?; Visualize filter shape | Filter plot (Figure 3 bài báo) | "Thay vì lưu toàn bộ vector h ∈ R^L, Hyena dùng FFN nhỏ để tính h_t tại mỗi bước..." | TV1 |
| **7** | Kết Quả Bài Báo Gốc | SotA attention-free trên WT103; Match Transformer 335M, -20% FLOPs; 100x speedup L=64K | Bảng kết quả Table 2/3; Speedup chart | "Bài gốc train 335M params — quá lớn với nhóm sinh viên. Nhóm chỉ tái hiện xu hướng..." | TV1 |
| **8** | Setup Thực Nghiệm Nhóm | WikiText-2 + Synthetic; Transformer-small vs Hyena-small (4 layers, d=256); E1–E3; Colab T4 | Bảng config 2 model | "Nhóm thu nhỏ scope: 4 layers, d_model=256, dataset ~2M tokens..." | TV2 |
| **9** | Kết Quả E1: Baseline | Loss curves Transformer vs Hyena; PPL table; Nhận xét | Loss curve plot; Bảng PPL | "Ở scale nhỏ, PPL của 2 model khá gần nhau — điều này nhất quán với kết quả bài gốc..." | TV3 |
| **10** | Kết Quả E2+E3: Scaling | Bảng time/memory vs L; Biểu đồ scaling | Scaling chart time; Scaling chart memory | "Hyena scale tốt hơn: khi L tăng 2x, time chỉ tăng ~2x thay vì 4x như Transformer..." | TV3 |
| **11** | Thảo Luận & Kết Luận | Ưu: subquadratic, long-context; Nhược: scale nhỏ ít lợi thế PPL; Tương lai: Mamba | Bảng ưu/nhược điểm | "Nhóm kết luận: Hyena là bước đột phá về efficiency, nhưng cần scale lớn để thấy rõ lợi thế ngôn ngữ..." | TV1 |
| **12** | Q&A + References | 6 tài liệu tham khảo chính; Link GitHub | QR code GitHub repo | "Cảm ơn thầy/cô và các bạn. Nhóm sẵn sàng trả lời câu hỏi." | Cả nhóm |

---

## 10. Câu Trả Lời Mẫu Cho Giảng Viên

---

### Câu hỏi 1: "Nhóm em làm gì trong đề tài này?"

> *[Trả lời trong 1–1.5 phút, giọng tự nhiên]*

"Dạ thưa thầy, nhóm em thực hiện đề tài khảo sát và tái hiện kiến trúc Hyena Hierarchy, dựa trên bài báo của Poli và cộng sự, được chấp nhận tại ICML 2023. Bài báo giải quyết hạn chế cốt lõi của Transformer: cơ chế Self-Attention có độ phức tạp O(L²) theo độ dài chuỗi, khiến mô hình không thể xử lý văn bản ngữ cảnh dài một cách hiệu quả. Hyena thay thế Attention bằng toán tử đệ quy kết hợp tích chập dài qua FFT và nhân cổng element-wise, đạt độ phức tạp O(N·L log L) — thực sự dưới bậc hai. Nhóm em không tái hiện toàn bộ bài báo — vì bài gốc train 335 triệu tham số trên dữ liệu 825GB — mà thực hiện small-scale reproduction: train và so sánh Transformer-small và Hyena-small trên dataset WikiText-2, đánh giá perplexity, tốc độ huấn luyện và khả năng mở rộng theo sequence length. Mục tiêu của nhóm là xác nhận xu hướng: chất lượng ngôn ngữ tương đương ở scale nhỏ, nhưng Hyena có lợi thế rõ rệt về tốc độ và bộ nhớ khi sequence length tăng."

---

### Câu hỏi 2: "Dataset lấy từ đâu?"

> *[Trả lời trong 30–45 giây]*

"Dạ thưa thầy, nhóm em sử dụng dataset WikiText-2, được tải trực tiếp từ thư viện HuggingFace Datasets thông qua lệnh `load_dataset('wikitext', 'wikitext-2-raw-v1')`. Đây là benchmark chuẩn cho bài toán language modeling, được trích xuất từ các bài viết Wikipedia chất lượng cao và được tiền xử lý để giữ nguyên cấu trúc câu. Dataset gồm khoảng 2 triệu token cho tập train, 220 nghìn token cho tập validation và 245 nghìn token cho tập test. Nhóm chọn WikiText-2 thay vì WikiText-103 như bài gốc vì giới hạn tài nguyên — tuy nhiên dataset này đủ nhỏ để chạy trên Google Colab, trong khi vẫn đủ lớn để huấn luyện mô hình ngôn ngữ và quan sát xu hướng. Ngoài ra, nhóm cũng tự tạo một synthetic recall task nhỏ để kiểm tra khả năng xử lý phụ thuộc dài hạn — đây là một trong những điểm mạnh lý thuyết của Hyena."

---

### Câu hỏi 3: "Các em tái hiện bài báo gốc như thế nào?"

> *[Trả lời trong 45–60 giây]*

"Dạ thưa thầy, nhóm em tiếp cận theo hướng trend verification thay vì exact reproduction. Cụ thể, nhóm tự cài đặt hai mô hình nhỏ trong PyTorch: Transformer-small và Hyena-small, mỗi mô hình có 4 layers, d_model bằng 256, tổng số tham số khoảng 5–10 triệu — nhỏ hơn bài gốc khoảng 30 lần. Đối với Hyena, nhóm cài đặt phiên bản đơn giản hóa dùng FFT thuần Python thay vì CUDA kernel tùy chỉnh, nhưng vẫn giữ đúng logic toán học của recurrence và implicit filter. Nhóm huấn luyện cả hai mô hình trên WikiText-2 với cùng hyperparameter, sau đó so sánh validation perplexity, thời gian huấn luyện mỗi bước và bộ nhớ GPU khi tăng sequence length từ 256 lên 512 và 1024. Nhóm nhận thức rõ rằng kết quả perplexity ở scale nhỏ có thể không phản ánh đầy đủ kết quả bài gốc — điều này được giải thích rõ trong phần thảo luận của báo cáo. Điều quan trọng là nhóm quan sát được xu hướng: Hyena scale tốt hơn về thời gian và bộ nhớ khi sequence length tăng, nhất quán với lý thuyết O(N·L log L)."

---

## 11. Kết Quả Đầu Ra Cuối Cùng Cần Nộp

| # | Sản phẩm | Format | Phụ trách | Deadline |
|---|---|---|---|---|
| 1 | **Báo cáo** | PDF, ≥15 trang, 10 sections | TV1 (chủ biên) | Cuối Tuần 3 |
| 2 | **Slide thuyết trình** | PDF hoặc PPTX, 10–12 slide | Cả nhóm | Cuối Tuần 3 |
| 3 | **Source code / Notebook** | `.py` + `.ipynb` trên GitHub | TV2 + TV3 | Cuối Tuần 3 |
| 4 | **README hướng dẫn chạy** | Markdown, đủ để setup từ đầu | TV2 | Cuối Tuần 3 |
| 5 | **Bảng kết quả thực nghiệm** | CSV + embed trong báo cáo | TV3 | Cuối Tuần 3 |
| 6 | **Link dataset** | HuggingFace URL trong README | TV2 | Cuối Tuần 1 |
| 7 | **Tài liệu tham khảo** | IEEE/APA format trong báo cáo | TV1 | Cuối Tuần 3 |

### Danh sách nộp tối thiểu (minimum viable)

```
📁 Nộp gồm:
  ├── report.pdf
  ├── slides.pdf
  ├── GitHub repo URL (public)
  │   ├── README.md
  │   ├── requirements.txt
  │   ├── data/preprocess.py
  │   ├── models/transformer.py
  │   ├── models/hyena.py
  │   ├── train.py
  │   ├── evaluate.py
  │   ├── results/E1_baseline.csv
  │   └── notebooks/02_model_training.ipynb
  └── results/plots/ (≥2 biểu đồ)
```

---

*Tài liệu này được tổng hợp từ phân tích bài báo Poli et al. (2023) và hướng dẫn thực nghiệm cho nhóm sinh viên CS2308. Cập nhật: 06/2026.*
