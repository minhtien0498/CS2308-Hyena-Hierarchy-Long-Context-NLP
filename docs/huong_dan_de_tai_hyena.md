# Hướng Dẫn Đề Tài: Hyena Hierarchy — Khảo Sát và Tái Hiện Kiến Trúc
**Môn: CS2308 – Chuyên đề Nghiên cứu và Ứng dụng về Xử lý Ngôn ngữ Tự nhiên**
**Bài báo gốc:** *Hyena Hierarchy: Towards Larger Convolutional Language Models* (Poli et al., ICML 2023)

---

## Mục lục

1. [Tổng quan bài báo](#1-tổng-quan-bài-báo)
2. [Liên hệ với môn Chuyên đề NLP](#2-liên-hệ-với-môn-chuyên-đề-nlp)
3. [Nhóm sinh viên cần làm gì?](#3-nhóm-sinh-viên-cần-làm-gì)
4. [Dataset sử dụng](#4-dataset-sử-dụng)
5. [Kế hoạch thực nghiệm](#5-kế-hoạch-thực-nghiệm)
6. [Output cuối cùng của nhóm](#6-output-cuối-cùng-của-nhóm)
7. [Cấu trúc báo cáo đề xuất](#7-cấu-trúc-báo-cáo-đề-xuất)
8. [Cấu trúc slide đề xuất](#8-cấu-trúc-slide-đề-xuất)
9. [Rủi ro và cách thu hẹp phạm vi](#9-rủi-ro-và-cách-thu-hẹp-phạm-vi)
10. [Câu trả lời ngắn cho thầy](#10-câu-trả-lời-ngắn-cho-thầy)

---

## 1. Tổng Quan Bài Báo

### 1.1 Bài báo giải quyết vấn đề gì?

Bài báo giải quyết **bottleneck quadratic complexity của Self-Attention** trong Transformer khi xử lý chuỗi dài (long sequences). Với input có độ dài `L`, self-attention tiêu tốn `O(L²)` cả về tính toán lẫn bộ nhớ — điều này khiến Transformer trở nên **cực kỳ đắt đỏ** khi `L` lên đến hàng nghìn hoặc hàng chục nghìn token.

**Câu hỏi trung tâm của bài báo:**
> *Liệu có thể thiết kế một toán tử dưới bậc hai (subquadratic) thay thế self-attention, đạt chất lượng tương đương Transformer trên các benchmark ngôn ngữ lớn, mà không cần hybridization với attention?*

### 1.2 Vì sao Self-Attention gặp hạn chế với chuỗi dài?

Self-attention có thể biểu diễn dưới dạng:

```
y = A(k, q) · v
```

trong đó `A` là **attention matrix** có kích thước `L × L`, được tính từ linear projections `q`, `k`, `v` của input.

**Ba đặc tính của attention:**
| Đặc tính | Mô tả | Hệ quả |
|---|---|---|
| **Data-controlled** | Ma trận `A` phụ thuộc vào input | Mạnh nhưng tốn kém |
| **Sublinear parameters** | Chỉ cần 3 ma trận chiếu (Q, K, V) | Tiết kiệm tham số |
| **Unrestricted context** | Mỗi token có thể attend vào mọi token khác | Linh hoạt nhưng `O(L²)` |

**Vấn đề cụ thể:**
- **Bộ nhớ:** Cần lưu ma trận attention `L × L` → tăng bậc hai theo độ dài chuỗi
- **Thời gian tính toán:** `O(L²)` FLOP mỗi lần forward pass
- **Thực tế:** Ở `L = 8192`, standard attention trong PyTorch **hết RAM**. FlashAttention cải thiện nhưng vẫn giữ độ phức tạp `O(L²)` về tính toán
- **Cản trở long-context:** Không thể train với context window hàng chục nghìn token trên GPU thông thường

### 1.3 Hyena được đề xuất như thế nào?

**Hyena Hierarchy** là một toán tử truy hồi (recurrence) kết hợp hai nguyên thủy đơn giản:

```
Hyena recurrence (order N):
  z^(n+1)_t = x^n_t · (h^n * z^n)_t     với n = 1, ..., N
  y_t = z^(N+1)_t
```

Tức là: tại mỗi bước `n` của recurrence, **nhân element-wise** một phép tính tích chập dài với một projection của input.

**Hai nguyên thủy:**
1. **Long convolution** `h * z`: tích chập trên toàn bộ độ dài chuỗi, thực hiện qua FFT trong `O(L log L)` thay vì `O(L²)`
2. **Element-wise multiplicative gating** `x^n · (·)`: nhân từng vị trí, `O(L)` — cho phép mô hình "chọn lọc" thông tin dựa trên input

**Đặc điểm nổi bật:**
- **Subquadratic:** Toàn bộ Hyena chạy trong `O(N · L log₂ L)` thay vì `O(L²)`
- **Data-controlled:** Giống attention, output của Hyena phụ thuộc vào input thông qua các gating projections
- **Unbounded context:** Không bị giới hạn bởi local window, có thể học phụ thuộc dài hạn

### 1.4 Các khái niệm chính

#### Long Convolution
Tích chập dài là phép toán giữa một filter `h` và input `u` **trên toàn bộ độ dài chuỗi** `L`, không bị giới hạn bởi kích thước kernel nhỏ như CNN thông thường.

- **FIR (Explicit filters):** Lưu trực tiếp các giá trị `h_t` → `O(ML)` → bị ràng buộc bởi M ≪ L
- **Implicit filters (dùng trong Hyena):** Parametrize filter bằng một mạng FFN nhỏ: `h_t = Window(t) · FFN(PositionalEncoding(t))` → tách biệt độ dài filter khỏi số tham số → có thể có filter độ dài `L` với số tham số nhỏ

#### Gating (Element-wise Multiplication)
Gating là phép nhân từng phần tử: `output_t = gate_t · value_t`. Trong Hyena, các projections `x^1, x^2, ..., x^N` của input đóng vai trò là **data-controlled gates**, cho phép mô hình học cách "lọc" thông tin dựa trên nội dung thực tế của chuỗi.

#### Implicit Filter (Bộ lọc ngầm)
Thay vì học trực tiếp vector `h ∈ R^L`, Hyena học một **hàm số** `γ_θ: t → h_t` được parametrize bởi FFN:
```
h_t = Window(t) · FFN(PositionalEncoding(t))
```
Ưu điểm: số tham số O(1) so với độ dài chuỗi, nhưng filter có thể dài tùy ý.

#### Subquadratic Complexity
Hyena chạy trong `O(N · L log₂ L)` nhờ dùng FFT cho tích chập dài. So sánh:
- Standard attention: `O(L²)`
- FlashAttention: `O(L²)` tính toán (tối ưu bộ nhớ, không tính toán)
- Hyena: `O(L log L)` ← thực sự subquadratic

Kết quả thực nghiệm từ bài báo:
- `5x` speedup so với standard attention ở `L = 8192`
- `2x` speedup so với FlashAttention ở `L = 8192`
- `100x` speedup so với FlashAttention ở `L = 64K` (nơi standard attention hết RAM)

### 1.5 Đóng góp chính của bài báo

| # | Đóng góp | Chi tiết |
|---|---|---|
| 1 | **Hyena Hierarchy operator** | Toán tử subquadratic mới, kết hợp long conv + gating, đạt chất lượng gần Transformer |
| 2 | **Implicit long convolution** | Parametrize filter bằng FFN, tách biệt độ dài khỏi số tham số |
| 3 | **Matrix decomposition view** | Chỉ ra Hyena tương đương decomposition của data-controlled matrix (tổng quát hóa H3, GSS) |
| 4 | **Benchmark on WikiText-103 & The Pile** | SotA cho attention-free architectures; match Transformer ở 335M với ít FLOPs hơn 20% |
| 5 | **Long-context efficiency** | 100x speedup tại L=64K; mở đường cho long-context language models |
| 6 | **Generality** | Áp dụng được cho cả vision (ViT → HyenaViT), không chỉ NLP |

---

## 2. Liên Hệ Với Môn Chuyên Đề NLP

### 2.1 Đề tài thuộc phần nào trong NLP?

Đề tài này nằm ở **giao thoa của nhiều chủ đề quan trọng trong NLP hiện đại**:

```
┌─────────────────────────────────────────────────────┐
│                  Language Modeling                   │
│  (Autoregressive LM, perplexity, WikiText, The Pile) │
└───────────────────────┬─────────────────────────────┘
                        │
        ┌───────────────▼────────────────┐
        │  Transformer & Self-Attention   │
        │  (Q, K, V, attention matrix,   │
        │   causal masking, O(L²))       │
        └───────────────┬────────────────┘
                        │  ← Hyena giải quyết vấn đề này
        ┌───────────────▼────────────────┐
        │  Efficient Transformer /        │
        │  Alternatives to Attention      │
        │  (Linear Attention, SSM,        │
        │   Hyena, Mamba, RWKV)          │
        └───────────────┬────────────────┘
                        │
        ┌───────────────▼────────────────┐
        │      Long-Context NLP           │
        │  (Context window >1K tokens,   │
        │   long-range dependencies)     │
        └───────────────┬────────────────┘
                        │
        ┌───────────────▼────────────────┐
        │  Convolutional Sequence Models  │
        │  (CNNs, SSM, S4, CKConv,      │
        │   Hyena as generalization)     │
        └─────────────────────────────────┘
```

### 2.2 Vì sao phù hợp với môn Chuyên đề NLP?

**Lý do về mặt lý thuyết:**
- Đây là một trong những **hướng nghiên cứu nóng nhất (2022–2024)** trong NLP: thoát khỏi sự phụ thuộc vào attention
- Bài báo xuất hiện tại ICML 2023 — top-tier venue trong ML/NLP
- Hyena là tiền thân trực tiếp của **Mamba (2023)** — một trong những kiến trúc được quan tâm nhất hiện nay
- Cho phép sinh viên hiểu sâu **tại sao attention hoạt động và tại sao nó không thể scale**

**Lý do về mặt kỹ năng:**
- Rèn luyện kỹ năng **đọc bài báo khoa học** (paper reading)
- Thực hành **reproduction** — một kỹ năng quan trọng trong nghiên cứu
- Làm quen với **PyTorch**, FFT, và các khái niệm signal processing trong NLP
- Hiểu cách đo lường và so sánh mô hình: perplexity, FLOPs, memory

**Lý do về mặt thực tiễn:**
- Code Hyena có trên GitHub (repo `hazyresearch/safari`)
- Dataset nhỏ (WikiText-2) chạy được trên Google Colab
- Kết quả so sánh trực quan (loss curves, bảng so sánh)

---

## 3. Nhóm Sinh Viên Cần Làm Gì?

> **Nguyên tắc quan trọng:** Nhóm KHÔNG cần tái hiện toàn bộ bài báo gốc (train 335M parameters trên The Pile). Phạm vi hợp lý là **survey + small-scale reproduction** để kiểm chứng xu hướng.

### 3.1 Phân chia công việc theo từng phần

---

#### 📚 Phần 1: Đọc hiểu bài báo (1–2 tuần)
**Mục tiêu:** Mọi thành viên hiểu rõ bài báo gốc trước khi code.

| Task | Nội dung | Output |
|---|---|---|
| Đọc Abstract + Introduction | Hiểu vấn đề bài toán | Ghi chú tóm tắt |
| Đọc Section 2 (Preliminaries) | Hiểu FIR, IIR, SSM, convolution | Mind map các khái niệm |
| Đọc Section 3 (Hyena Operator) | Hiểu recurrence, implicit filter, algorithm | Sơ đồ kiến trúc tự vẽ |
| Đọc Section 4 (Experiments) | Hiểu setup, dataset, kết quả | Bảng kết quả tóm tắt |
| Đọc Related Work | Biết vị trí Hyena trong landscape | Bảng so sánh với SSM, H3 |

---

#### 🧠 Phần 2: Nền tảng Transformer / Self-Attention (1 tuần)
**Mục tiêu:** Hiểu rõ baseline Transformer để có cơ sở so sánh.

| Task | Nội dung |
|---|---|
| Self-attention mechanics | Q, K, V, softmax, scaled dot-product |
| Causal masking | Cách mask lower-triangular để LM autoregressive |
| Transformer block | MHA + FFN + LayerNorm + residual |
| Complexity analysis | Tại sao `O(L²)` về time và memory |
| Tham khảo | "Attention Is All You Need" (Vaswani et al., 2017) |

---

#### ⚙️ Phần 3: Tìm hiểu Hyena Operator (1–2 tuần)
**Mục tiêu:** Hiểu kiến trúc Hyena đủ để cài đặt hoặc đọc code.

| Task | Nội dung |
|---|---|
| Long convolution via FFT | Convolution theorem, `O(L log L)` |
| Implicit filter (FFN-based) | Tại sao dùng FFN để parametrize filter |
| Hyena recurrence | Vẽ sơ đồ cho N=2 (Hyena²) |
| So sánh với H3 và SSM | Hyena tổng quát hóa H3 như thế nào |
| Đọc code Hyena | Repo `hazyresearch/safari` hoặc `state-spaces/hyena-dna` |

---

#### 📦 Phần 4: Chuẩn bị Dataset (3–5 ngày)
**Mục tiêu:** Có dataset sạch, tokenized, sẵn sàng để train.

| Task | Nội dung |
|---|---|
| Tải WikiText-2 hoặc subset WikiText-103 | HuggingFace Datasets |
| Tokenize với GPT-2 tokenizer | BPE tokenizer, vocabulary size |
| Tạo data loader | Sliding window, sequence chunking |
| Viết preprocessing script | Có thể tái sử dụng |

---

#### 🏗️ Phần 5: Cài đặt mô hình Baseline (1–2 tuần)
**Mục tiêu:** Có một Transformer-small và Hyena-small chạy được.

| Task | Nội dung |
|---|---|
| Transformer-small | GPT-like: 2–4 layers, 4 heads, d_model=128/256 |
| Hyena block | 1 Hyena layer hoặc model ghép Hyena blocks |
| Training loop | Cross-entropy loss, AdamW, learning rate schedule |
| Evaluation | Perplexity = exp(validation loss) |
| Logging | TensorBoard hoặc Weights & Biases |

---

#### 🔬 Phần 6: Chạy Thực nghiệm (1–2 tuần)
**Mục tiêu:** Có bảng số liệu để so sánh.

| Thí nghiệm | Nội dung |
|---|---|
| Exp-1: Transformer vs Hyena ở L=256 | Train cả hai, so sánh loss + perplexity |
| Exp-2: Scale sequence length | Chạy L=256, 512, 1024 với cùng model |
| Exp-3: Memory + time | Đo GPU memory và training time per epoch |
| (Optional) Exp-4: Synthetic recall task | Đo khả năng recall ở sequence dài |

---

#### 📊 Phần 7: Đánh giá Kết quả (1 tuần)
**Mục tiêu:** Phân tích, giải thích số liệu.

| Task | Nội dung |
|---|---|
| Vẽ loss curves | Training loss + val loss theo epoch |
| Bảng so sánh | Transformer vs Hyena: perplexity, time, memory |
| Phân tích xu hướng | Khi L tăng, Hyena có lợi thế gì? |
| Giới hạn | Tại sao kết quả có thể khác bài gốc? |

---

#### 📝 Phần 8: Viết Báo cáo và Làm Slide (1–2 tuần)
**Mục tiêu:** Sản phẩm học thuật hoàn chỉnh.

| Task | Nội dung |
|---|---|
| Viết báo cáo | Theo cấu trúc Section 7 |
| Làm slide | Theo cấu trúc Section 8 |
| Chuẩn bị GitHub repo | Code + README + notebook |
| Rehearsal thuyết trình | Tập thuyết trình trước nhóm |

---

## 4. Dataset Sử Dụng

### 4.1 Dataset trong bài báo gốc

| Dataset | Vai trò | Quy mô |
|---|---|---|
| **WikiText-103** | Language modeling benchmark | 103M tokens, vocabulary 267K |
| **The Pile** | Large-scale LM pretraining | 825GB văn bản đa dạng |
| **Synthetic recall tasks** | Kiểm tra khả năng long-context | Tự tạo: copy, associative recall |

### 4.2 Dataset đề xuất cho nhóm sinh viên

---

#### 🟢 WikiText-2 *(Khuyến nghị chính)*
- **Nguồn:** `datasets.load_dataset("wikitext", "wikitext-2-raw-v1")` (HuggingFace)
- **Quy mô:** ~2M tokens training, ~220K validation, ~245K test
- **Vai trò:** Dataset chuẩn để train và đánh giá language model
- **Ưu điểm:**
  - Cực nhỏ, tải trong vài giây
  - Chuẩn benchmark (có thể so sánh với nhiều bài báo khác)
  - Chạy tốt trên Colab Free (T4 GPU)
  - Đủ để thấy sự khác biệt giữa Transformer và Hyena
- **Hạn chế:**
  - Quá nhỏ để thấy long-context advantage rõ ràng
  - Perplexity có thể không thấp như bài gốc (dataset khác nhau)
- **Phù hợp Colab:** ✅ Hoàn toàn phù hợp

---

#### 🟡 WikiText-103 (Subset 10–20%)
- **Nguồn:** `datasets.load_dataset("wikitext", "wikitext-103-raw-v1")`
- **Quy mô subset:** ~10–20M tokens (lấy 10–20% đầu)
- **Vai trò:** Gần hơn với bài gốc, vẫn manageable
- **Ưu điểm:**
  - Cùng dataset với bài báo gốc → số liệu có thể tham chiếu
  - Phong phú hơn WT2
- **Hạn chế:**
  - Train lâu hơn WT2 (~3–5x)
  - Cần Colab Pro hoặc máy có GPU tốt
- **Phù hợp Colab:** ⚠️ Cần Colab Pro hoặc thời gian train lâu hơn

---

#### 🟡 TinyStories
- **Nguồn:** `datasets.load_dataset("roneneldan/TinyStories")`
- **Quy mô:** ~470M tokens (nhưng có thể lấy 10% = ~47M)
- **Vai trò:** Dataset truyện ngắn đơn giản, ngôn ngữ dễ học
- **Ưu điểm:**
  - Ngôn ngữ tự nhiên, không quá phức tạp
  - Mô hình nhỏ học tốt hơn
- **Hạn chế:**
  - Không phải benchmark chuẩn → khó so sánh với bài gốc
  - Có thể quá dễ, không thấy sự khác biệt rõ ràng
- **Phù hợp Colab:** ✅ Nếu chỉ dùng subset

---

#### 🟠 Penn Treebank (PTB)
- **Nguồn:** `datasets.load_dataset("ptb_text_only")`
- **Quy mô:** ~1M tokens
- **Vai trò:** Classic benchmark, dùng ở nhiều bài cũ
- **Ưu điểm:**
  - Rất nhỏ, chạy cực nhanh
  - Có thể train nhiều lần để debug
- **Hạn chế:**
  - Dataset cũ, không còn được dùng nhiều trong nghiên cứu hiện đại
  - Vocabulary giới hạn (10K), không thể hiện hết khả năng của mô hình
- **Phù hợp Colab:** ✅ Rất phù hợp để debug

---

#### 🟢 Synthetic Copy/Recall Task *(Đề xuất thêm vào)*
- **Nguồn:** Tự tạo (20–30 dòng code Python)
- **Vai trò:** Kiểm tra khả năng nhớ thông tin dài hạn (long-context capability)
- **Cách tạo:**
  ```python
  # Ví dụ: Associative Recall
  # Input:  [A→1, B→2, C→3, ..., query: B→?]
  # Output: 2
  ```
- **Ưu điểm:**
  - Kiểm tra đúng điểm mạnh của Hyena (long-range dependency)
  - Kết quả rõ ràng: chính xác hay không?
  - Có thể kiểm soát độ dài sequence và độ khó
- **Hạn chế:**
  - Không phải benchmark thực tế NLP
  - Chỉ dùng để illustration
- **Phù hợp Colab:** ✅ Hoàn toàn

### 4.3 Khuyến nghị dataset cho nhóm

```
Ưu tiên sử dụng:
  1. WikiText-2      → Train/eval chính
  2. Synthetic task  → Demo long-context advantage
  3. (Optional) WikiText-103 subset → Nếu có đủ GPU
```

---

## 5. Kế Hoạch Thực Nghiệm

### 5.1 Bảng kế hoạch thực nghiệm

| # | Tên thí nghiệm | Dataset | Model | Seq Length | Metrics | Kết quả kỳ vọng |
|---|---|---|---|---|---|---|
| **E1** | Baseline comparison | WikiText-2 | Transformer-small vs Hyena-small | 256 | Train loss, Val loss, PPL | Cả hai converge; PPL tương đương ±10% |
| **E2** | Scale sequence length (Transformer) | WikiText-2 | Transformer-small | 256 → 512 → 1024 | Training time/step, GPU memory | Time và memory tăng bậc hai |
| **E3** | Scale sequence length (Hyena) | WikiText-2 | Hyena-small | 256 → 512 → 1024 → 2048 | Training time/step, GPU memory | Time và memory tăng gần tuyến tính (L log L) |
| **E4** | Memory comparison | WikiText-2 | Transformer vs Hyena | 256, 512, 1024 | Peak GPU memory (MB) | Hyena dùng ít memory hơn ở L lớn |
| **E5** | Long-context recall | Synthetic | Transformer vs Hyena | 256, 512, 1024 | Accuracy (%) | Hyena maintain accuracy tốt hơn |

### 5.2 Cấu hình mô hình đề xuất

```python
# Transformer-small
config_transformer = {
    "n_layers": 4,
    "n_heads": 4,
    "d_model": 256,
    "d_ff": 1024,
    "vocab_size": 50257,  # GPT-2 tokenizer
    "max_seq_len": 1024,
    "dropout": 0.1,
}

# Hyena-small (equivalent size)
config_hyena = {
    "n_layers": 4,
    "hyena_order": 2,       # Hyena² (equivalent to H3)
    "d_model": 256,
    "d_ff": 1024,
    "filter_order": 64,     # FFN size for implicit filter
    "vocab_size": 50257,
    "max_seq_len": 1024,
    "dropout": 0.1,
}
```

### 5.3 Training setup

```python
# Training hyperparameters
training_config = {
    "optimizer": "AdamW",
    "lr": 1e-3,
    "weight_decay": 0.1,
    "batch_size": 16,       # Điều chỉnh theo GPU memory
    "max_epochs": 20,
    "warmup_steps": 200,
    "gradient_clip": 1.0,
    "device": "cuda" if torch.cuda.is_available() else "cpu",
}
```

### 5.4 Cách đo metrics

```python
# Perplexity
import math
perplexity = math.exp(validation_loss)

# GPU Memory
import torch
peak_memory_mb = torch.cuda.max_memory_allocated() / 1024**2

# Time per step
import time
start = time.time()
# ... training step ...
time_per_step = time.time() - start
```

### 5.5 Kết quả kỳ vọng (định tính)

Nhóm nên kỳ vọng **thấy xu hướng** chứ không phải số liệu chính xác như bài gốc:

| Tiêu chí | Transformer | Hyena | Xu hướng |
|---|---|---|---|
| Perplexity (WT2, L=256) | Baseline | Tương đương ±10% | Ngang nhau |
| Training time (L tăng 2x) | Tăng ~4x | Tăng ~2x | Hyena có lợi hơn |
| GPU Memory (L tăng 2x) | Tăng ~4x | Tăng ~2x | Hyena có lợi hơn |
| Long-context recall | Giảm dần | Ổn định hơn | Hyena có lợi hơn |

> **Lưu ý:** Với model nhỏ và dataset nhỏ, kết quả PPL có thể không thấy sự khác biệt rõ ràng — điều này là **bình thường** và cần được giải thích trong báo cáo.

---

## 6. Output Cuối Cùng Của Nhóm

| # | Sản phẩm | Mô tả | Format |
|---|---|---|---|
| 1 | **Báo cáo tổng quan** | Tài liệu học thuật đầy đủ | PDF, ~15–25 trang |
| 2 | **Slide thuyết trình** | 10–12 slide, rõ ràng, có hình | PDF/PPTX, 15–20 phút |
| 3 | **Code/Notebook thực nghiệm** | Jupyter notebook chạy được | `.ipynb` trên GitHub |
| 4 | **Dataset preprocessing script** | Script tokenize, tạo dataloader | `preprocess.py` |
| 5 | **Bảng kết quả so sánh** | E1–E5 với số liệu thực | Có trong báo cáo và slide |
| 6 | **Nhận xét ưu/nhược điểm** | Phân tích Hyena vs Transformer | Có trong báo cáo Section 8 |
| 7 | **README** | Hướng dẫn chạy code | `README.md` trên GitHub |

### 6.1 Cấu trúc GitHub repo đề xuất

```
hyena-reproduction/
├── README.md
├── requirements.txt
├── data/
│   └── preprocess.py          # Script tiền xử lý
├── models/
│   ├── transformer.py         # Transformer-small
│   └── hyena.py              # Hyena-small
├── train.py                   # Training loop
├── evaluate.py                # Evaluation
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_model_training.ipynb
│   └── 03_results_analysis.ipynb
├── results/
│   ├── E1_baseline_comparison.csv
│   ├── E2_transformer_scale.csv
│   └── E3_hyena_scale.csv
└── report/
    └── report.pdf
```

---

## 7. Cấu Trúc Báo Cáo Đề Xuất

### Mục lục báo cáo

---

#### 1. Giới thiệu (~2 trang)
**Cần viết:**
- Bối cảnh: Transformer đang thống trị NLP nhưng có hạn chế về độ phức tạp
- Vấn đề: Self-attention `O(L²)` cản trở long-context processing
- Mục tiêu đề tài: Khảo sát Hyena Hierarchy như một giải pháp thay thế
- Đóng góp của nhóm (survey + small reproduction)
- Cấu trúc báo cáo

---

#### 2. Cơ Sở Lý Thuyết (~4 trang)
**Cần viết:**
- **2.1 Language Modeling:** Định nghĩa LM autoregressive, perplexity
- **2.2 Transformer và Self-Attention:** Kiến trúc, attention formula, Multi-Head Attention
- **2.3 Causal Masking:** Tại sao cần mask trong LM
- **2.4 Convolution:** FIR, IIR, discrete convolution, FFT
- **2.5 State Space Models (SSM):** S4, Mamba, liên hệ với Hyena
- **2.6 Alternatives to Attention:** Tổng quan landscape (Linear Attention, Performer, H3, Hyena, Mamba)

---

#### 3. Bài Báo Hyena Hierarchy (~4 trang)
**Cần viết:**
- **3.1 Motivation:** Tại sao cần thay thế attention?
- **3.2 Hyena Operator:** Định nghĩa recurrence, công thức toán học
- **3.3 Implicit Long Convolution:** Parametrize filter bằng FFN
- **3.4 Hyena Matrix View:** Giải thích decomposition của data-controlled matrix
- **3.5 Complexity Analysis:** Chứng minh `O(N · L log L)`
- **3.6 Kết quả bài gốc:** Tóm tắt bảng kết quả từ bài báo (WikiText-103, The Pile)

---

#### 4. Phương Pháp Tái Hiện (~2 trang)
**Cần viết:**
- **4.1 Phạm vi tái hiện:** Giải thích tại sao chọn small-scale
- **4.2 Kiến trúc Transformer-small:** Cấu hình, số tham số
- **4.3 Kiến trúc Hyena-small:** Cấu hình, cách cài đặt Hyena block
- **4.4 Sự khác biệt với bài gốc:** Dataset khác nhau, model nhỏ hơn

---

#### 5. Dataset và Tiền Xử Lý (~2 trang)
**Cần viết:**
- **5.1 Dataset được chọn:** WikiText-2 và synthetic task
- **5.2 Thống kê dataset:** Số token, vocabulary, phân phối
- **5.3 Tokenization:** BPE tokenizer (GPT-2), vocabulary size
- **5.4 Data pipeline:** Cách tạo sequences, batch, dataloader

---

#### 6. Thiết Lập Thực Nghiệm (~1–2 trang)
**Cần viết:**
- **6.1 Môi trường:** Python version, PyTorch version, GPU sử dụng
- **6.2 Hyperparameters:** Learning rate, batch size, epochs, optimizer
- **6.3 Metrics đánh giá:** Perplexity, training time, memory
- **6.4 Danh sách thí nghiệm:** E1–E5 với mô tả ngắn

---

#### 7. Kết Quả và Đánh Giá (~3 trang)
**Cần viết:**
- **7.1 E1: Baseline comparison:** Loss curves, PPL bảng
- **7.2 E2 & E3: Scale sequence length:** Bảng time + memory
- **7.3 E4: Memory comparison:** Biểu đồ memory vs L
- **7.4 E5: Long-context recall:** Bảng accuracy
- **7.5 Nhận xét:** Xu hướng quan sát được

---

#### 8. Thảo Luận (~2 trang)
**Cần viết:**
- **8.1 Ưu điểm của Hyena:** Subquadratic, không cần attention
- **8.2 Nhược điểm của Hyena:** Cần train lâu hơn ở scale nhỏ, implicit filter khó debug
- **8.3 Giới hạn của reproduction:** Dataset nhỏ, model nhỏ → kết quả không đại diện đầy đủ
- **8.4 Hướng phát triển:** Mamba, Mamba-2, RWKV, RetNet

---

#### 9. Kết Luận (~0.5 trang)
**Cần viết:**
- Tóm tắt đóng góp của nhóm
- Kết luận về Hyena so với Transformer
- Hướng nghiên cứu tiếp theo

---

#### 10. Tài Liệu Tham Khảo
**Phải có tối thiểu:**
- Poli et al. (2023) — Hyena Hierarchy (bài chính)
- Vaswani et al. (2017) — Attention Is All You Need
- Gu et al. (2021) — S4
- Dao et al. (2022) — H3
- Dao et al. (2022) — FlashAttention
- Merity et al. (2016) — WikiText dataset

---

## 8. Cấu Trúc Slide Đề Xuất

### Slide deck: ~11 slide, 15–20 phút

---

#### Slide 1: Trang bìa
- **Nội dung:** Tên đề tài, tên nhóm, môn học, ngày thuyết trình
- **Hình:** Logo trường, hình minh họa neural network
- **Ghi chú:** Giới thiệu nhóm và đề tài ngắn gọn

---

#### Slide 2: Động lực và Vấn đề (Motivation)
- **Nội dung:**
  - "Transformer thống trị NLP từ 2017"
  - Hạn chế: `O(L²)` attention → không thể scale lên context dài
  - Số liệu: "Ở L=64K, PyTorch attention → OOM"
- **Hình:** Biểu đồ complexity so sánh `O(L²)` vs `O(L log L)` vs `O(L)`
- **Ghi chú:** Giải thích vấn đề bằng ngôn ngữ đơn giản, dùng ví dụ

---

#### Slide 3: Self-Attention Recap
- **Nội dung:**
  - Formula: `Attention(Q,K,V) = softmax(QKᵀ/√d)V`
  - Ma trận attention `L×L`
  - 3 đặc tính: data-controlled, sublinear params, unrestricted context
- **Hình:** Sơ đồ attention matrix (ô vuông L×L)
- **Ghi chú:** Nhắc lại nhanh cho audience đã biết Transformer

---

#### Slide 4: Các Giải Pháp Thay Thế (Landscape)
- **Nội dung:**
  - Timeline: Linear Attention → Performer → S4 → H3 → **Hyena** → Mamba
  - Bảng so sánh: SSM vs Attention vs Hyena
- **Hình:** Timeline diagram hoặc bảng so sánh
- **Ghi chú:** Đặt Hyena trong context nghiên cứu, không cần đi sâu từng cái

---

#### Slide 5: Hyena Hierarchy — Ý tưởng chính
- **Nội dung:**
  - "Hyena = Long Convolution + Gating"
  - Recurrence: `z^(n+1) = x^n · (h^n * z^n)`
  - Order N=2: Hyena² ≈ H3
- **Hình:** Sơ đồ recurrence từ bài báo (Figure 1)
- **Ghi chú:** Đây là slide trọng tâm — cần giải thích kỹ

---

#### Slide 6: Implicit Long Convolution Filter
- **Nội dung:**
  - Filter `h_t = Window(t) · FFN(PositionalEncoding(t))`
  - Tại sao implicit tốt hơn explicit?
  - Visualize filter shape (exponential decay + high-frequency)
- **Hình:** Figure 3 từ bài báo (filter visualization)
- **Ghi chú:** Nhấn mạnh: "số tham số nhỏ nhưng filter dài tùy ý"

---

#### Slide 7: Complexity Analysis
- **Nội dung:**
  - Hyena: `O(N · L log₂ L)` vs Attention: `O(L²)`
  - Speedup theo bài báo: 5x ở L=8192, 100x ở L=64K
  - Biểu đồ runtime từ bài báo
- **Hình:** Figure về speedup từ bài báo gốc
- **Ghi chú:** Trả lời câu hỏi: "Tại sao Hyena nhanh hơn?"

---

#### Slide 8: Kết Quả Bài Báo Gốc
- **Nội dung:**
  - WikiText-103: Hyena SotA attention-free
  - The Pile (335M): Match Transformer với ít FLOPs hơn 20%
  - ImageNet: Hyena-ViT match standard ViT
- **Hình:** Bảng kết quả từ bài báo (Table 2, 3)
- **Ghi chú:** Giải thích tại sao đây là milestone quan trọng

---

#### Slide 9: Thiết Lập Thực Nghiệm Của Nhóm
- **Nội dung:**
  - Dataset: WikiText-2 + Synthetic recall task
  - Model: Transformer-small vs Hyena-small (4 layers, d=256)
  - Experiments E1–E5
  - Hardware: Google Colab T4
- **Hình:** Bảng cấu hình model, cấu trúc kiến trúc
- **Ghi chú:** Giải thích tại sao chọn scale nhỏ

---

#### Slide 10: Kết Quả Thực Nghiệm
- **Nội dung:**
  - Bảng E1: PPL Transformer vs Hyena
  - Biểu đồ E2+E3: Time/Memory vs Sequence Length
  - Bảng E5: Recall accuracy
- **Hình:** Loss curves, memory/time scaling chart
- **Ghi chú:** Nhấn mạnh xu hướng, không chỉ số tuyệt đối

---

#### Slide 11: Thảo Luận và Kết Luận
- **Nội dung:**
  - Ưu điểm Hyena: subquadratic, long-context capable
  - Nhược điểm: cần scale lớn để thấy rõ lợi thế PPL
  - Hướng tương lai: Mamba, Mamba-2
  - Kết luận nhóm
- **Hình:** Bảng ưu/nhược điểm đơn giản
- **Ghi chú:** "Hyena là bước đột phá, nhưng Mamba đã đơn giản hóa hơn nữa"

---

#### Slide 12 (Optional): Q&A + References
- **Nội dung:** Danh sách tài liệu tham khảo chính
- **Hình:** Logo bài báo hoặc QR code GitHub repo

---

## 9. Rủi Ro và Cách Thu Hẹp Phạm Vi

### 9.1 Bảng rủi ro và giải pháp

| Rủi ro | Mức độ | Giải pháp |
|---|---|---|
| **Bài gốc nặng về toán** (FFT, SSM, butterfly decomposition) | 🔴 Cao | Chỉ cần hiểu ở mức "functional": input → output là gì, tại sao nhanh hơn. Không cần chứng minh toán học đầy đủ |
| **Code Hyena khó cài** (CUDA kernels, flash_fft_conv) | 🔴 Cao | Dùng pure-Python FFT implementation đơn giản thay vì CUDA. Hoặc dùng repo `hyena-dna` nhỏ hơn |
| **The Pile quá lớn** (825GB) | 🟢 Thấp | Không cần dùng The Pile. WikiText-2 là đủ cho mục đích so sánh xu hướng |
| **Không đủ GPU** | 🟡 Trung bình | Google Colab Free (T4) đủ cho model nhỏ (d=128, 4 layers, L=512). Cần quản lý batch size |
| **Kết quả không giống bài gốc** | 🟡 Trung bình | Đây là **bình thường** và cần được giải thích trong báo cáo. Mục tiêu là thấy xu hướng, không phải tái hiện số chính xác |
| **Hyena converge chậm hơn** ở scale nhỏ | 🟡 Trung bình | Train đủ epoch, dùng learning rate scheduling tốt |
| **Thời gian không đủ** | 🟠 Có thể | Ưu tiên E1 + E2+E3 trước. E4, E5 là bonus |

### 9.2 Chiến lược thu hẹp phạm vi theo mức độ tài nguyên

#### Nếu chỉ có Colab Free (T4, ~15GB RAM)
```
✅ Làm được:
  - WikiText-2, d_model=128, 4 layers, L=256/512
  - E1: Baseline comparison
  - E2+E3: Scale L (256→512→1024 với batch nhỏ hơn)
  
⚠️ Giới hạn:
  - L=2048 có thể cần batch_size=1–2
  - Training time ~30 phút/epoch
```

#### Nếu có Colab Pro (A100, 40GB RAM)
```
✅ Làm được thêm:
  - d_model=256, 6 layers
  - L lên đến 4096
  - WikiText-103 subset
  - E4, E5 đầy đủ
```

#### Nếu chỉ có CPU
```
⚠️ Thu hẹp tối đa:
  - PTB dataset (nhỏ nhất)
  - d_model=64, 2 layers, L=128/256
  - Chỉ E1 và E2 (định tính)
  - Tập trung vào phần survey/lý thuyết
```

### 9.3 Minimum viable reproduction (tối thiểu cần làm)

Nếu gặp khó khăn về tài nguyên, nhóm có thể tập trung vào:

1. **Lý thuyết hoàn chỉnh** (Section 1, 2, 3 của báo cáo) — 40% điểm
2. **Chạy ít nhất E1** (Transformer vs Hyena, WikiText-2, L=256) — 30% điểm
3. **Phân tích scaling lý thuyết** nếu không chạy được E2/E3 — 20% điểm
4. **Slide và thuyết trình** rõ ràng — 10% điểm

---

## 10. Câu Trả Lời Ngắn Cho Thầy

> **Khi thầy hỏi:** *"Nhóm em làm gì trong đề tài này?"*

---

**Đề tài của nhóm em tập trung vào khảo sát và tái hiện kiến trúc Hyena Hierarchy, được giới thiệu trong bài báo *"Hyena Hierarchy: Towards Larger Convolutional Language Models"* của Poli et al., được chấp nhận tại ICML 2023.**

**Bài toán chính mà bài báo giải quyết là hạn chế của cơ chế Self-Attention trong Transformer, vốn có độ phức tạp bậc hai O(L²) theo độ dài chuỗi, gây cản trở trong các bài toán ngôn ngữ ngữ cảnh dài. Hyena đề xuất thay thế Attention bằng một toán tử subquadratic kết hợp tích chập dài (long convolution) và nhân cổng (gating), chạy trong O(N · L log L) — cho phép xử lý chuỗi hàng chục nghìn token hiệu quả hơn.**

**Nhóm em sẽ thực nghiệm trên dataset WikiText-2 (từ HuggingFace), so sánh một mô hình Transformer nhỏ với một mô hình Hyena có cùng cấu hình tham số. Các chỉ số đánh giá bao gồm perplexity trên tập validation, thời gian huấn luyện và bộ nhớ GPU khi tăng độ dài sequence. Nhóm kỳ vọng quan sát được xu hướng: chất lượng ngôn ngữ tương đương nhau ở scale nhỏ, nhưng Hyena có lợi thế rõ rệt về tốc độ và bộ nhớ khi sequence length tăng lên.**

---

*Tài liệu này được biên soạn dựa trên bài báo Poli et al. (2023), ICML. Cập nhật lần cuối: 06/2026.*
