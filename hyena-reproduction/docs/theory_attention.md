# Transformer & Self-Attention — Cơ Sở Lý Thuyết
**Phụ trách:** Thành viên 1 (TV1) | **Deadline:** Cuối Tuần 1

---

## 1. Language Modeling

**Định nghĩa:** Language model (LM) học phân phối xác suất P(w₁, w₂, ..., wₙ) trên chuỗi từ.

**Autoregressive LM** phân tích chuỗi theo dạng:
```
P(w₁,...,wₙ) = P(w₁) · P(w₂|w₁) · P(w₃|w₁,w₂) · ... · P(wₙ|w₁,...,wₙ₋₁)
```

**Perplexity** — đo chất lượng LM:
```
PPL = exp(- 1/N · Σ log P(wₜ | w₁,...,wₜ₋₁))
```
- PPL thấp hơn = mô hình tốt hơn
- PPL = exp(validation_loss) trong PyTorch

---

## 2. Transformer Architecture

### 2.1 Tổng quan
Transformer (Vaswani et al., 2017) gồm:
```
Input Tokens → Token Embedding + Positional Embedding
            → N × Transformer Block
            → Layer Norm
            → LM Head (linear projection)
```

### 2.2 Transformer Block
```
TransformerBlock(x):
  x = x + MultiHeadAttention(LayerNorm(x))  ← Residual + Pre-LN
  x = x + FeedForward(LayerNorm(x))          ← Residual + Pre-LN
  return x
```

### 2.3 Self-Attention Mechanics

**Scaled Dot-Product Attention:**
```
Attention(Q, K, V) = softmax(Q·Kᵀ / √d_k) · V
```

**Các bước tính:**
1. Linear projections: Q = X·W_Q, K = X·W_K, V = X·W_V
2. Compute scores: S = Q·Kᵀ / √d_k   → shape (L, L)
3. Causal masking: S[i,j] = -∞ nếu j > i (đảm bảo causality)
4. Softmax: A = softmax(S)             → attention weights
5. Weighted sum: Output = A·V          → (L, d_model)

**Multi-Head Attention (MHA):**
- Chạy h lần attention song song với các W_Q, W_K, W_V khác nhau
- Concat kết quả → linear projection

### 2.4 Causal Masking
- Cần thiết cho **autoregressive** LM: token tại vị trí t chỉ được "thấy" t' ≤ t
- Thực hiện bằng cách đặt -∞ tại các vị trí future trong attention matrix
- Sau softmax, các vị trí future có weight = 0

---

## 3. Tại Sao Self-Attention O(L²)?

### 3.1 Bộ nhớ
- Ma trận attention S có kích thước **L × L**
- Mỗi layer cần lưu: L × L × 4 bytes = O(L²)
- Ví dụ: L=8192 → 8192² = 67M entries = ~256MB/layer

### 3.2 Thời gian tính toán
- Phép nhân Q·Kᵀ: O(L² · d_k)
- Softmax trên L×L: O(L²)
- Phép nhân A·V: O(L² · d_v)
- **Tổng: O(L² · d_model) per layer**

### 3.3 Scaling quan sát thực tế
| L | L² | Tăng L 2x → L² tăng |
|---|---|---|
| 256 | 65,536 | — |
| 512 | 262,144 | 4x |
| 1,024 | 1,048,576 | 4x |
| 4,096 | 16,777,216 | 4x |
| 8,192 | 67,108,864 | 4x |
| 64,000 | 4,096,000,000 | → OOM |

---

## 4. So Sánh Transformer vs Hyena

> *[TV1 điền cột Hyena sau khi đọc Section 3 của bài báo]*

| Tiêu chí | Transformer | Hyena |
|---|---|---|
| **Core operation** | Scaled dot-product attention | FFT convolution + element-wise gating |
| **Complexity (time)** | O(L²) per layer | O(N·L log L) per layer |
| **Complexity (memory)** | O(L²) | O(L) |
| **Context** | Unrestricted (attend any pair) | Unbounded (via long conv) |
| **Data-controlled** | ✅ Yes (Q, K, V depend on input) | ✅ Yes (gates x^n depend on input) |
| **Parameters** | W_Q, W_K, W_V (3 matrices) | FFN filter + projection matrices |
| **Causality** | Causal mask (lower triangular) | Causal conv (zero-padding) |
| **Parallelizable** | ✅ Fully parallel | ✅ Fully parallel (FFT) |
| **Long-context (L=64K)** | OOM | ✅ Runs fine |
| **Convergence speed** | Fast | Slightly slower at small scale |
| **Implementation** | Simple, well-optimized | Complex, less mature |

---

## 5. Tài Liệu Tham Khảo Cho Phần Này

- Vaswani et al. (2017). *Attention Is All You Need*. NeurIPS 2017.
  → Bài gốc của Transformer
- Illustrated Transformer: https://jalammar.github.io/illustrated-transformer/
  → Visualize rất tốt, khuyên đọc trước
- Poli et al. (2023). *Hyena Hierarchy*. ICML 2023. [Section 1, 2, 3]

---

*File này là output của Thành viên 1, Tuần 1. Cập nhật lần cuối: ___/2026*
