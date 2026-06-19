# Slide Outline — Hyena Hierarchy

**Môn:** CS2308 - Chuyên đề NLP  
**Bài báo:** *Hyena Hierarchy: Towards Larger Convolutional Language Models* - Poli et al., ICML 2023  
**Thời lượng:** 45 phút trình bày + 15 phút hỏi đáp  
**Số slide đề xuất:** 33 slide  
**Phân chia:** 3 thành viên, mỗi người khoảng 11 slide / 15 phút

---

## Tổng Quan Phân Chia

| Thành viên | Slide | Nội dung |
|---|---:|---|
| Kiên | 1-11 | Nền tảng, motivation, Self-Attention, related work |
| Tiến | 12-22 | Hyena operator, FFTConv, implicit filter, kết quả paper gốc |
| Quang | 23-33 | Reproduction của nhóm, thực nghiệm, thảo luận, kết luận |

---

## Kiên — Nền Tảng và Motivation

### Slide 1 — Trang Bìa

- Tên đề tài: Khảo sát và tái hiện kiến trúc Hyena Hierarchy.
- Tên bài báo, tác giả, venue ICML 2023.
- Tên nhóm, môn học, ngày trình bày.

### Slide 2 — Câu Hỏi Nghiên Cứu

- "Is attention all we need?"
- Có thể thay Self-Attention bằng một toán tử dưới bậc hai mà vẫn đạt chất lượng tương đương không?
- Dẫn vào mục tiêu của Hyena.

### Slide 3 — Vì Sao Long-Context Quan Trọng?

- Tài liệu dài, sách, code dài, hội thoại dài.
- Chuỗi sinh học, âm thanh, video, ảnh lớn.
- Long-context là yêu cầu thực tế nhưng Attention rất tốn kém.

### Slide 4 — Language Modeling Recap

- Autoregressive language modeling.
- Next-token prediction.
- Perplexity: PPL thấp hơn nghĩa là mô hình dự đoán tốt hơn.

### Slide 5 — Transformer Recap

- Token embedding + positional embedding.
- Transformer block: Self-Attention + FFN + residual.
- Self-Attention là core operation cần phân tích.

### Slide 6 — Self-Attention Mechanics

- Công thức: `Attention(Q,K,V) = softmax(QK^T / sqrt(d))V`.
- Q, K, V là projections từ input.
- Causal mask trong language modeling.

### Slide 7 — Attention Matrix

- Ma trận attention kích thước `L x L`.
- Mỗi token tương tác với các token trước đó.
- Hình minh họa: L tăng thì số ô tăng theo bình phương.

### Slide 8 — Bottleneck `O(L^2)`

- Time complexity: `O(L^2)`.
- Memory complexity: `O(L^2)`.
- Ví dụ: L tăng 2 lần thì số tương tác tăng khoảng 4 lần.

### Slide 9 — FlashAttention và Giới Hạn

- FlashAttention tối ưu memory access và giảm bộ nhớ thực tế.
- Nhưng compute vẫn là `O(L^2)`.
- Vẫn khó mở rộng tới context cực dài.

### Slide 10 — Capability Gap

- Attention có 3 tính chất mạnh:
  - Data control.
  - Sublinear parameter scaling.
  - Unrestricted context.
- Các phương pháp thay thế attention trước Hyena thường thiếu một phần các tính chất này.

### Slide 11 — Related Work

- Transformer.
- SSM/S4.
- H3/GSS.
- Hyena.
- Mamba.
- Mục tiêu: đặt Hyena vào dòng nghiên cứu attention-free / subquadratic models.

---

## Tiến — Phương Pháp Hyena và Kết Quả Bài Báo Gốc

### Slide 12 — Từ Attention Sang Hyena

- Nhắc lại vấn đề: cần toán tử rẻ hơn Attention.
- Nhưng vẫn cần data-controlled, context dài, ít tham số theo L.
- Hyena xây toán tử mới thay vì xấp xỉ trực tiếp attention matrix.

### Slide 13 — Ý Tưởng Chính

- Hyena = long convolution + element-wise gating.
- Long convolution mang thông tin toàn chuỗi.
- Gating giúp chọn lọc theo input.

### Slide 14 — Long Convolution

- Filter dài bằng toàn bộ sequence.
- Khác CNN local kernel.
- Có khả năng mô hình hóa phụ thuộc xa.

### Slide 15 — Data-Controlled Gating

- Gate `x^n` phụ thuộc vào input.
- Nhân element-wise với đầu ra convolution.
- Đây là cơ chế giúp Hyena không chỉ là convolution tĩnh.

### Slide 16 — Hyena Recurrence

```text
z^(n+1)_t = x^n_t * (h^n * z^n)_t
```

- `z^n`: trạng thái trung gian.
- `h^n`: long convolution filter.
- `x^n`: gate phụ thuộc input.

### Slide 17 — Order-N Hierarchy

- N là số bước recurrence.
- N càng lớn, toán tử càng biểu diễn phong phú hơn.
- Hyena bậc thấp liên hệ với H3/GSS.

### Slide 18 — Matrix View

- Gating tương ứng diagonal matrix.
- Convolution tương ứng Toeplitz matrix.
- Hyena là tích xen kẽ diagonal và Toeplitz matrices.

### Slide 19 — Implicit Filter

```text
h_t = Window(t) * FFN(PositionalEncoding(t))
```

- Không học trực tiếp vector filter dài L.
- Dùng FFN sinh filter theo vị trí.
- Tách số tham số khỏi độ dài sequence.

### Slide 20 — FFTConv

- Convolution trực tiếp tốn nhiều chi phí.
- Dùng FFT: `FFT -> multiply -> iFFT`.
- Complexity giảm về `O(L log L)`.

### Slide 21 — Complexity và Ý Nghĩa

| Toán tử | Time | Memory |
|---|---|---|
| Standard Attention | `O(L^2)` | `O(L^2)` |
| FlashAttention | `O(L^2)` compute | thấp hơn thực tế |
| Hyena | `O(N * L log L)` | gần tuyến tính theo L |

### Slide 22 — Kết Quả Paper Gốc

- Synthetic tasks: recall/reasoning dài.
- WikiText-103 và The Pile: match Transformer ở một số setting.
- Long-context speedup: nhanh hơn rõ ở L lớn.
- Nhấn mạnh: kết quả này là của paper gốc, không phải của nhóm.

---

## Quang — Reproduction và Thực Nghiệm Của Nhóm

### Slide 23 — Scope Của Nhóm

- Không tái hiện full paper vì tài nguyên rất lớn.
- Nhóm thực hiện small-scale reproduction.
- Mục tiêu là trend verification, không phải match số tuyệt đối.

### Slide 24 — Mục Tiêu Reproduction

- So sánh Transformer-small và Hyena-small.
- Đánh giá PPL/loss ở WikiText-2.
- Đo runtime/memory khi sequence length tăng.

### Slide 25 — Dataset

- WikiText-2.
- GPT-2 tokenizer.
- Sequence chunking theo `seq_len`.
- Train/validation/test split.

### Slide 26 — Pipeline

```text
Load WikiText-2 -> tokenize -> SequenceDataset -> DataLoader
-> train model -> evaluate PPL/runtime/memory
```

### Slide 27 — Transformer-Small

- GPT-like Transformer.
- Layers, heads, d_model, d_ff.
- Baseline để so sánh.

### Slide 28 — Hyena-Small

- HyenaLM trong repo.
- Order N=2.
- FFT-based, pure PyTorch.
- Không dùng custom CUDA kernel.

### Slide 29 — Training/Evaluation Setup

- Optimizer: AdamW.
- Metric: train loss, validation loss, perplexity.
- Runtime/memory đo bằng `evaluate.py --scaling`.
- Hardware cần ghi rõ: Colab T4/MPS/CPU.

### Slide 30 — Kết Quả E1: PPL/Loss

- Bảng Transformer vs Hyena tại L=256.
- Cần điền số thật từ CSV train/evaluate.
- Nếu chưa đủ epoch, ghi rõ là preliminary result.

### Slide 31 — Kết Quả Scaling

- Runtime/memory theo sequence length.
- Transformer: 256, 512, 1024.
- Hyena: 256, 512, 1024, 2048 nếu chạy được.
- Dùng `results/plots/reproduce_runtime.png` nếu phù hợp.

### Slide 32 — Thảo Luận và Giới Hạn

- Scale nhỏ nên PPL có thể chưa phản ánh ưu thế của Hyena.
- Pure PyTorch FFT có overhead, nhất là ở sequence ngắn.
- Không có custom FFTConv/CUDA kernel như paper.
- Kết quả nhóm chỉ minh họa xu hướng.

### Slide 33 — Kết Luận & Q&A

- Attention không phải con đường duy nhất.
- Hyena là một hướng attention-free quan trọng.
- Small-scale reproduction giúp nhóm hiểu trend và giới hạn thực tế.
- Chuyển sang Q&A.

---

## Output Thực Nghiệm Cần Có Trước Khi Làm Slide

| Mức | Output | Dùng cho slide |
|---|---|---|
| Bắt buộc | Bảng setup dataset/model/hardware | 25-29 |
| Bắt buộc | E1: train/evaluate Transformer-small và Hyena-small tại L=256 | 30 |
| Bắt buộc | Ít nhất một bảng runtime scaling cho hai model | 31 |
| Nên có | Plot loss/PPL hoặc runtime | 30-31 |
| Bonus | Memory comparison hoặc synthetic recall | 31-32 |

---

## Lệnh Gợi Ý Cho TV3

```bash
# E1: Train baseline tại L=256
python train.py --model transformer --seq_len 256 --epochs 5 --batch_size 16
python train.py --model hyena --seq_len 256 --epochs 5 --batch_size 16

# E2/E3: Runtime scaling, không cần checkpoint
python evaluate.py --model transformer --scaling --seq_lens 256 512 1024 --batch_size 8
python evaluate.py --model hyena --scaling --seq_lens 256 512 1024 2048 --batch_size 8
```

Nếu không đủ thời gian/GPU, có thể giảm `epochs`, `batch_size`, hoặc chỉ chạy `seq_lens 256 512 1024` cho cả hai model. Khi trình bày phải ghi rõ đây là kết quả preliminary.
