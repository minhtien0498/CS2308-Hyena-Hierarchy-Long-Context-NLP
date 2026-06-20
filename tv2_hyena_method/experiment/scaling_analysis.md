# TV2 - Scaling Analysis (E2/E3, đồng bộ với `results/`)

> Phục vụ yêu cầu [phan_cong_present_hyena_3_tuan.md §8.3](../../phan_cong_present_hyena_3_tuan.md):
> *"CSV scaling E2/E3: TV3 tạo + TV2 phân tích scaling runtime/memory và liên hệ complexity."*
>
> **Lưu ý phụ trách:** TV2 từng dùng bộ số tạm thời để viết khung phân tích. File này đã được **đồng bộ lại theo CSV chính thức trong `results/`** để TV2 và TV3 cùng dùng một bộ số.

---

## 1. Điều Kiện Chạy

| | Giá trị |
|---|---|
| Lệnh | `python evaluate.py --model {transformer,hyena} --scaling --seq_lens ... --batch_size 8` |
| d_model | 256 · n_layers 4 · batch 8 · dropout 0.0 |
| Device | **Colab T4 (CUDA)** |
| Đo | warmup 5 + measure 20 forward pass, dummy input |
| Tham số | Transformer 16.28M / Hyena 16.45M (chênh ~1%, so sánh công bằng) |
| File | [E2_transformer_scale.csv](E2_transformer_scale.csv), [E3_hyena_scale.csv](E3_hyena_scale.csv) |
| Nguồn số | đồng bộ từ [results/](../../results/) |

---

## 2. Kết Quả Thô

### E2 — Transformer (Attention)

| L | Time/step (ms) | Tăng / nhân đôi L | Throughput (k tok/s) | Peak mem (MB) |
|---:|---:|---|---:|---:|
| 256 | 21.41 | — | 95.7 | 466.3 |
| 512 | 43.71 | **2.04x** | 93.7 | 862.7 |
| 1024 | 100.14 | **2.29x** | 81.8 | 1654.8 |

256→1024 (x4 L): time tăng **4.68x**.

### E3 — Hyena

| L | Time/step (ms) | Tăng / nhân đôi L | Throughput (k tok/s) | Peak mem (MB) |
|---:|---:|---|---:|---:|
| 256 | 21.85 | — | 93.7 | 466.7 |
| 512 | 42.38 | **1.94x** | 96.7 | 862.3 |
| 1024 | 84.07 | **1.98x** | 97.4 | 1651.4 |
| 2048 | 167.82 | **2.00x** | 97.6 | 3231.9 |

256→1024 (x4 L): time tăng **3.85x**.

---

## 3. Đọc Số — 3 Điểm Chính

### 3.1 Tỉ lệ scaling khớp lý thuyết hơn bản MPS cũ
- **Hyena ~2.0x mỗi lần nhân đôi L** (1.94 -> 1.98 -> 2.00) -> rất sát dấu hiệu `O(L log L)`.
- **Transformer tăng nhanh hơn** (2.04 -> 2.29) và có xu hướng tiếp tục cong thêm khi `L` lớn hơn; dải này chưa đủ lớn để thấy mức 4x rõ nét của `O(L^2)`, nhưng quãng 256->1024 đã cao hơn Hyena.

### 3.2 Throughput: Hyena gần như phẳng, Transformer bắt đầu giảm

| | L=256 | L=1024 | Biến động |
|---|---:|---:|---|
| Transformer | 95.7 k tok/s | 81.8 k tok/s | **-14.5%** |
| Hyena | 93.7 k tok/s | 97.4 k tok/s | **gần phẳng** (+4.0%) |

-> Với bộ số Colab/CUDA mới, Hyena không còn bị "đứt throughput" ở dải vừa; đường throughput gần như nằm ngang, trong khi Transformer giảm rõ khi `L` tăng. Xem [scaling_throughput.png](scaling_throughput.png).

### 3.3 Điểm crossover
Tại L=256 Hyena **hơi chậm hơn** (21.85 vs 21.41 ms), nhưng tới L=512 Hyena đã **nhanh hơn** (42.38 vs 43.71 ms) và giữ lợi thế tại L=1024 (84.07 vs 100.14 ms). Nghĩa là **crossover nằm trong khoảng 256-512**; trên lưới đo hiện tại, **L=512 là điểm đầu tiên Hyena vượt Transformer**. Xem [scaling_time.png](scaling_time.png).

-> Điều này hợp với lập luận paper: ở `L` nhỏ overhead FFT vẫn còn, nhưng khi `L` tăng thêm thì lợi thế `O(L log L)` bắt đầu lộ ra.

---

## 4. So Với Paper & Giới Hạn (trung thực)

| | Paper gốc | Kết quả nhóm |
|---|---|---|
| Crossover vs attention | ~L 2048 | giữa L 256-512 |
| Crossover vs FlashAttention | L 4096-8192 | không đo (không có FlashAttn) |
| Speedup @ L 64K | ~100x | ngoài tầm (chỉ chạy tới L 2048) |

**Crossover của nhóm sớm hơn paper** — khả năng cao vì: (1) quy mô model nhỏ, (2) dải `L` ngắn, (3) implementation Hyena là pure-PyTorch FFT, (4) baseline attention không phải kernel tối ưu như hệ thống benchmark trong paper. Vì vậy, đây là bằng chứng **định tính đúng xu hướng**, không phải đối chiếu số tuyệt đối 1-1 với paper.

### Giới hạn cần ghi trên slide
- **Memory giờ đã đo được** vì CSV mới đến từ CUDA; tuy nhiên Transformer mới có tới `L=1024`, nên chưa có đối sánh memory đầy đủ với Hyena tại `L=2048`.
- Pure PyTorch FFT, không có custom CUDA kernel -> Hyena vẫn chịu overhead ở `L` nhỏ.
- `d_model=256`, ~16M params, `L <= 2048` — vẫn là small-scale reproduction.
- Chạy benchmark quy mô nhỏ, không có lặp nhiều seed/nhiều lần -> không báo cáo khoảng tin cậy.

---

## 5. Câu Nói Cho Slide 21/22 (TV2) và Slide 31 (TV3)

> "Trong bộ số đã đồng bộ trên Colab T4, Hyena chỉ chậm hơn Transformer rất nhẹ ở L=256, nhưng đến L=512 đã bắt đầu nhanh hơn. Mỗi lần nhân đôi sequence length, time của Hyena tăng gần 2x, rất sát xu hướng `O(L log L)`, trong khi Transformer tăng nhanh hơn và throughput giảm từ 95.7 xuống 81.8k token/s. Vì vậy, dù đây mới là reproduction quy mô nhỏ và chưa có kernel tối ưu, nhóm vẫn quan sát được xu hướng cốt lõi của paper: khi context dài lên, Hyena scale dễ hơn Attention."

---

## 6. Bug Cần Báo Nhóm (lặp lại)
[evaluate.py:33](../../../evaluate.py#L33) import `get_dataloader` ở top-level -> nhánh `--scaling` (không cần data) bị phụ thuộc `datasets`/`transformers`. Đề xuất TV3 chuyển import vào nhánh E1. Chi tiết: [expected_complexity.md §6](expected_complexity.md).
