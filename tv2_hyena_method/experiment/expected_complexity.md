# TV2 - Complexity Kỳ Vọng (lý thuyết, trước khi chạy số)

> Phục vụ yêu cầu [phan_cong_present_hyena_3_tuan.md §8.2](../../phan_cong_present_hyena_3_tuan.md): bảng complexity kỳ vọng để đối chiếu với kết quả scaling (E2/E3).

---

## 1. Complexity Theo Lý Thuyết

| Toán tử | Time / layer | Memory / layer | Ghi chú |
|---|---|---|---|
| Standard Attention | `O(L² · d)` | `O(L²)` | materialize attention matrix `L×L` |
| FlashAttention | `O(L²)` compute | tối ưu memory access (vẫn bậc hai) | không giảm FLOP |
| Hyena (order N) | `O(N · d · L · log L)` | `O(d · L)` | không tạo ma trận `L×L` |

Với config nhóm: `d=256`, `N=2` → Hyena ≈ `O(2 · 256 · L · log₂L)`.

> Paper Proposition 3.2 ghi chính xác `O(N·D·L·(log₂L + D))`. Ở slide ta dùng dạng rút gọn `O(N·L·log L)` cho trực giác.

---

## 2. Tỉ Lệ Tăng Khi `L` Tăng 2 Lần

| | Khi `L → 2L` | Vì sao |
|---|---|---|
| Attention time | tăng **~4×** | `(2L)² / L² = 4` |
| Hyena time | tăng **~2×** | `2L·log(2L) / (L·log L) ≈ 2 · (log L + 1)/log L → 2` khi `L` lớn |

→ Đây là mốc đối chiếu với số thực: nếu Transformer tăng ~4× và Hyena tăng ~2× khi nhân đôi `L`, thì xu hướng khớp lý thuyết.

---

## 3. Giá Trị Lý Thuyết Tại Các `L` Thử

Bậc tính (đơn vị tương đối, lấy log₂):

| L | L² (Attention) | L·log₂L (Hyena) | Tỉ lệ Attention/Hyena |
|---:|---:|---:|---:|
| 256 | 65 536 | 2 048 | ~32× |
| 512 | 262 144 | 4 608 | ~57× |
| 1 024 | 1 048 576 | 10 240 | ~102× |
| 2 048 | 4 194 304 | 22 528 | ~186× |

> Tỉ lệ "lý thuyết" tăng nhanh theo `L`, nhưng **số đo thực tế sẽ không khớp tuyệt đối** vì các lý do bên dưới.

---

## 4. Vì Sao Số Thực Có Thể Lệch Lý Thuyết

| Yếu tố | Tác động | Hướng |
|---|---|---|
| Pure PyTorch FFT (không CUDA kernel) | overhead FFT lớn | làm Hyena chậm hơn kỳ vọng ở `L` nhỏ/trung |
| Thư viện FFT tối ưu chung | chưa tinh chỉnh cho d_model=256 | tăng overhead cố định |
| MPS / CPU thay vì GPU | khác throughput & memory pool | sai khác tuyệt đối |
| Memory đo được chỉ khi có CUDA | `peak_mem_mb` trả 0 trên MPS/CPU ([evaluate.py:147](../../../evaluate.py#L147)) | cột memory có thể trống → đo riêng |
| Batch size cố định | che mờ chi phí theo `L` | giữ batch_size=8 đều cho 2 model |

---

## 5. Cái Nhìn Dự Kiến (pre-registration)

Trước khi xem số, kỳ vọng hợp lý cho reproduction nhóm:

1. **Time scaling:** Transformer tăng ~4× / nhân đôi L; Hyena tăng chậm hơn (~2–3×).
2. **Crossover:** ở `L` nhỏ (256–512), Hyena **có thể chậm hơn** Transformer do FFT overhead trên pure PyTorch. Lợi thế rõ hơn ở `L ≥ 1024`.
3. **Memory:** trên MPS/CPU cột `peak_mem_mb` có thể = 0 (chỉ CUDA đo được) → cần đo riêng hoặc ghi rõ hạn chế.
4. **PPL (E1, tách riêng):** chênh lệch có thể không rõ ở ~16M params.

> Đây là "kỳ vọng trước khi xem kết quả" (pre-registration) để tránh giải thích RESULTS chọn lọc. Sau khi chạy, đối chiếu tại [scaling_analysis.md](scaling_analysis.md).

---

## 6. Bug Cần Báo Nhóm

[evaluate.py:33](../../../evaluate.py#L33) import `from data.preprocess import get_dataloader` ở **top-level**, kéo theo `datasets` + `transformers` dù nhánh `--scaling` (chỉ dùng dummy input) không cần data.

→ Hệ quả: chạy `python evaluate.py --scaling` trên môi trường thiếu `datasets`/`transformers` sẽ **crash ngay lúc import**, dù logic scaling không đụng tới data.

**Đề xuất fix (để báo TV3):** chuyển import `get_dataloader` vào trong nhánh `else` (chỉ E1 cần), hoặc dùng lazy import. Khi đó `--scaling` chạy được trên môi trường chỉ có torch.
