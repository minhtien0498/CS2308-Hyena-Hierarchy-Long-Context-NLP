# TV2 - Scaling Analysis (E2/E3, số thật)

> Phục vụ yêu cầu [phan_cong_present_hyena_3_tuan.md §8.3](../../phan_cong_present_hyena_3_tuan.md):
> *"CSV scaling E2/E3: TV3 tạo + TV2 phân tích scaling runtime/memory và liên hệ complexity."*
>
> **Lưu ý phụ trách:** CSV do lệnh `evaluate.py --scaling` sinh (TV2 đã chạy vì TV3 chưa nộp). Phần **phân tích + liên hệ complexity là của TV2**. Khi TV3 chạy lại trên GPU/Colab, thay số vào đây — mạch phân tích giữ nguyên.

---

## 1. Điều Kiện Chạy

| | Giá trị |
|---|---|
| Lệnh | `python evaluate.py --model {transformer,hyena} --scaling --seq_lens ... --batch_size 8` |
| d_model | 256 · n_layers 4 · batch 8 · dropout 0.0 |
| Device | **MPS** (Apple Silicon), torch 2.12 |
| Đo | warmup 5 + measure 20 forward pass, dummy input |
| Tham số | Transformer 16.28M / Hyena 16.45M (chênh ~1%, so sánh công bằng) |
| File | [E2_transformer_scale.csv](E2_transformer_scale.csv), [E3_hyena_scale.csv](E3_hyena_scale.csv) |
| Ngày chạy | 15/06/2026 |

---

## 2. Kết Quả Thô

### E2 — Transformer (Attention)

| L | Time/step (ms) | Tăng / nhân đôi L | Throughput (k tok/s) |
|---:|---:|---|---:|
| 256 | 17.31 | — | 118.3 |
| 512 | 49.83 | **2.88×** | 82.2 |
| 1024 | 149.38 | **3.00×** | 54.8 |

256→1024 (×4 L): time tăng **8.63×**.

### E3 — Hyena

| L | Time/step (ms) | Tăng / nhân đôi L | Throughput (k tok/s) |
|---:|---:|---|---:|
| 256 | 33.29 | — | 61.5 |
| 512 | 65.57 | **1.97×** | 62.5 |
| 1024 | 131.70 | **2.01×** | 62.2 |
| 2048 | 276.21 | **2.10×** | 59.3 |

256→1024 (×4 L): time tăng **3.95×**.

---

## 3. Đọc Số — 3 Điểm Chính

### 3.1 Tỉ lệ scaling khớp lý thuyết
- **Hyena ~2.0× mỗi lần nhân đôi L** (1.97 → 2.01 → 2.10) → đúng dấu hiệu `O(L log L)`.
- **Transformer ~2.9–3.0× và đang tăng** (2.88 → 3.00) → tiến dần về 4× đặc trưng của `O(L²)` khi `L` lớn; ở `L` nhỏ component tuyến tính (FFN, embedding) làm giảm tỉ lệ.

### 3.2 Throughput: chênh rõ nhất
Đây là hình minh họa mạnh nhất cho slide:

| | L=256 | L=1024 | Giảm |
|---|---:|---:|---|
| Transformer | 118.3 k tok/s | 54.8 k tok/s | **−54%** |
| Hyena | 61.5 k tok/s | 62.2 k tok/s | **gần phẳng** (dao động ±4%) |

→ Throughput Hyena gần như **không đổi** khi `L` tăng (vì `time ∝ L log L` ⇒ `throughput = L/time ∝ 1/log L` giảm chậm), trong khi Transformer **sụp** theo `1/L`. Xem [scaling_throughput.png](scaling_throughput.png).

### 3.3 Điểm crossover
Tại L=512 Hyena **chậm hơn** (65.6 vs 49.8 ms); tại L=1024 Hyena **nhanh hơn** (131.7 vs 149.4 ms). **Crossover ≈ L 750–1000** (plot báo L=1024 — điểm đầu tiên Hyena vượt). Xem [scaling_time.png](scaling_time.png).

→ Bên dưới crossover, Hyena chậm hơn vì overhead FFT trên pure-PyTorch; bên trên, lợi thế `O(L log L)` bắt đầu vượt `O(L²)`.

---

## 4. So Với Paper & Giới Hạn (trung thực)

| | Paper gốc | Kết quả nhóm |
|---|---|---|
| Crossover vs attention | ~L 2048 | ~L 750–1024 |
| Crossover vs FlashAttention | L 4096–8192 | không đo (không có FlashAttn) |
| Speedup @ L 64K | ~100× | ngoài tầm (chỉ chạy tới L 2048) |

**Crossover của nhóm sớm hơn paper** — khả năng cao vì: (1) attention trên MPS cũng có overhead, (2) dải `L` nhỏ, (3) FFT pure-PyTorch chưa tối ưu. Đây là quan sát **định tính đúng xu hướng** (Hyena thắng khi `L` lớn), không phải tái hiện số tuyệt đối.

### Giới hạn cần ghi trên slide
- **Memory = 0.0 ở mọi L**: [evaluate.py:147](../../../evaluate.py#L147) chỉ đo memory qua `torch.cuda.max_memory_allocated()` → MPS/CPU trả 0. **Phải đo riêng** (ví dụ `torch.mps` hoặc chạy trên CUDA) nếu muốn có cột memory.
- Pure PyTorch FFT, không CUDA kernel → overhead lớn ở `L` nhỏ.
- `d_model=256`, ~16M params, `L ≤ 2048` — chưa đủ lớn để thấy speedup bùng nổ kiểu paper.
- Chạy 1 lần, không lặp seed → không có khoảng tin cậy.

---

## 5. Câu Nói Cho Slide 21/22 (TV2) và Slide 31 (TV3)

> "Ở quy mô nhỏ với FFT thuần PyTorch, Hyena chậm hơn Transformer khi `L` nhỏ do overhead FFT. Nhưng khi `L` tăng, thời gian Hyena chỉ tăng khoảng **2× mỗi lần nhân đôi** — đúng lý thuyết `O(L log L)` — trong khi Attention tăng khoảng **3× và đang tiến lên 4×**. Throughput Hyena gần phẳng (~60k token/s) còn Transformer giảm từ 118k xuống 55k. Điểm giao nhau rơi vào khoảng L≈1K. Đây là minh chứng định tính cho lợi thế long-context của Hyena, đúng xu hướng paper gốc, dù số tuyệt đối chưa so được vì scale nhỏ và thiếu kernel tối ưu."

---

## 6. Bug Cần Báo Nhóm (lặp lại)
[evaluate.py:33](../../../evaluate.py#L33) import `get_dataloader` ở top-level → nhánh `--scaling` (không cần data) bị phụ thuộc `datasets`/`transformers`. Đề xuất TV3 chuyển import vào nhánh E1. Chi tiết: [expected_complexity.md §6](expected_complexity.md).
