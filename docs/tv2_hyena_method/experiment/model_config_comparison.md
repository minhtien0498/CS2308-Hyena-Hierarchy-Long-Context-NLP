# TV2 - Bảng So Sánh Cấu Hình Transformer-small vs Hyena-small

> Phục vụ yêu cầu [phan_cong_present_hyena_3_tuan.md §8.2](../../phan_cong_present_hyena_3_tuan.md):
> *"Output cần nộp: Bảng cấu hình Transformer-small vs Hyena-small; đảm bảo so sánh công bằng."*

Mục đích: chứng minh hai model reproduction **so sánh công bằng** — cùng quy mô, chỉ khác cơ chế trộn sequence (attention vs Hyena operator).

---

## 1. Bảng Cấu Hình

Nguồn số liệu: [models/transformer.py](../../../models/transformer.py), [models/hyena.py](../../../models/hyena.py), [evaluate.py](../../../evaluate.py) (`build_model_fresh`).

| Tham số | Transformer-small | Hyena-small | Giống/khác |
|---|---|---|---|
| vocab_size | 50 257 (GPT-2 BPE) | 50 257 | ✅ giống |
| d_model | 256 | 256 | ✅ giống |
| n_layers (blocks) | 4 | 4 | ✅ giống |
| d_ff | 1 024 | 1 024 | ✅ giống |
| max_seq_len | 1 024 | 1 024 | ✅ giống |
| dropout (train) | 0.1 | 0.1 | ✅ giống |
| dropout (scaling test) | 0.0 | 0.0 | ✅ giống |
| **Cơ chế trộn sequence** | Multi-Head Attention (n_heads=4) | Hyena operator (order=2) | ❌ khác |
| n_heads / order | n_heads = 4 | order N = 2 | — |
| filter_dim (implicit filter FFN) | — | 64 | riêng Hyena |
| Embedding | token + positional | token + positional | ✅ giống |
| Block | Pre-LN + mix + Pre-LN + FFN + residual | giống, thay MHA bằng HyenaOperator | ✅ giống khung |
| LM head | Linear + weight tying | Linear + weight tying | ✅ giống |

> Khung block **giống hệt** ([transformer.py TransformerBlock](../../../models/transformer.py), [hyena.py HyenaBlock](../../../models/hyena.py#L270)): cùng Pre-LN, cùng FFN GELU, cùng residual. Khác duy nhất: lớp trộn sequence (MHA ↔ HyenaOperator). Đây là điều kiện cần để kết luận PPL/scaling chênh lệch là do **cơ chế**, không do quy mô.

---

## 2. Số Tham Số (đo thật)

Đo bằng `sum(p.numel() for p in model.parameters())`, không cần train:

| Model | Tham số | Tỉ lệ |
|---|---:|---|
| Transformer-small | **16 283 392** (~16.28M) | baseline |
| Hyena-small | **16 449 536** (~16.45M) | +1.0% so với Transformer |

**Kết luận so sánh công bằng:** hai model chênh nhau **~1%** tham số → đủ nhỏ để kết luận sự khác biệt PPL/runtime đến từ kiến trúc, không phải quy mô.

---

## 3. So Với Paper Gốc

| | Paper gốc | Nhóm |
|---|---|---|
| Params (WikiText-103 / The Pile) | 125M – 335M | ~16M |
| Tỉ lệ thu nhỏ | — | **~8–20× nhỏ hơn** |
| FFTConv | CUDA kernel tối ưu (`flash_fft_conv`) | `torch.fft.rfft` thuần (PyTorch) |
| Dataset | WikiText-103 / The Pile (825GB) | WikiText-2 (~2M tokens) |

> Hệ quả (cần nói trên slide giới hạn): ở ~16M params + pure PyTorch FFT, PPL chưa chắc phản ánh ưu thế của Hyena; lợi thế runtime chỉ rõ khi `L` lớn. Xem [expected_complexity.md](expected_complexity.md).

---

## 4. Lệnh Khởi Tạo Model (đối chiếu)

```python
# evaluate.py -> build_model_fresh
TransformerLM(vocab_size=50257, d_model=256, n_layers=4,
              n_heads=4, d_ff=1024, max_seq_len=seq_len, dropout=0.0)

HyenaLM(vocab_size=50257, d_model=256, n_layers=4,
        order=2, filter_dim=64, d_ff=1024,
        max_seq_len=seq_len, dropout=0.0)
```

Cùng `seq_len`, cùng `batch_size` khi đo scaling → kiểm soát biến nhiễu.
