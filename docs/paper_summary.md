# Paper Summary — Hyena Hierarchy: Towards Larger Convolutional Language Models
**Phụ trách:** Thành viên 1 (TV1) | **Deadline:** Cuối Tuần 1

> **Hướng dẫn:** Điền vào các mục [ ] sau khi đọc bài báo poli23a.pdf

---

## 1. Thông Tin Bài Báo

| Trường | Thông tin |
|---|---|
| **Tên bài** | Hyena Hierarchy: Towards Larger Convolutional Language Models |
| **Tác giả** | Michael Poli, Stefano Massaroli, Eric Nguyen, et al. |
| **Venue** | ICML 2023 (International Conference on Machine Learning) |
| **Year** | 2023 |
| **Link** | [poli23a.pdf] (file trong thư mục dự án) |
| **Code** | https://github.com/HazyResearch/safari |

---

## 2. Motivation — Vấn Đề Bài Báo Giải Quyết

> **Bối cảnh:** Kiến trúc Transformer đã đạt được những thành công vang dội trong xử lý ngôn ngữ tự nhiên. Tuy nhiên, nó gặp phải một giới hạn nghiêm trọng về hiệu năng khi xử lý các chuỗi văn bản dài do độ phức tạp tính toán và bộ nhớ tăng theo hàm bậc hai $O(L^2)$ của cơ chế Self-Attention. Bài báo Hyena Hierarchy tìm cách thiết kế một toán tử subquadratic thay thế Attention, vừa duy trì được hiệu suất ngôn ngữ của Transformer, vừa có khả năng mở rộng tối ưu lên các chuỗi cực dài.

**Vấn đề chính:**
Self-Attention trong Transformer có độ phức tạp O(L²) theo độ dài chuỗi L, gây ra:
- **Hạn chế về memory:** Ma trận attention kích thước $L \times L$ yêu cầu lưu trữ bộ nhớ tăng theo hàm bậc hai $O(L^2)$, nhanh chóng gây ra hiện tượng tràn bộ nhớ (Out-Of-Memory - OOM) trên các GPU hiện đại khi độ dài chuỗi tăng lên hàng nghìn hoặc chục nghìn token.
- **Hạn chế về tốc độ:** Phép tính nhân ma trận $Q K^T$ và softmax trên ma trận attention yêu cầu số lượng phép tính dấu phẩy động (FLOPs) tăng theo tỷ lệ bậc hai $O(L^2)$, tạo ra điểm nghẽn nghiêm trọng về thời gian xử lý (throughput) ở cả hai pha huấn luyện và suy luận.
- **Hạn chế về ứng dụng long-context:** Cản trở việc áp dụng mô hình vào các tác vụ đòi hỏi ngữ cảnh dài hạn như phân tích tài liệu dài, sinh mã nguồn, xử lý thông tin sinh học (DNA/protein) hoặc xử lý video độ phân giải cao.

**Câu hỏi nghiên cứu trung tâm:**
> "Liệu có thể thiết kế toán tử subquadratic thay thế attention, đạt chất lượng tương đương Transformer trên large-scale LM, không cần hybridization?"

---

## 3. Contribution — Đóng Góp Chính

> Các đóng góp chính của bài báo (theo Section 1):

| # | Đóng góp | Mô tả ngắn |
|---|---|---|
| 1 | **Hyena Hierarchy operator** | Đề xuất toán tử subquadratic mới thay thế self-attention, kết hợp phép tích chập dài (long convolution) và nhân cổng element-wise (gating) đệ quy, thu hẹp khoảng cách chất lượng (quality gap) với Transformer mà không cần lai (hybridize) với attention. |
| 2 | **Implicit long convolution** | Mô hình hóa bộ lọc tích chập dài dưới dạng hàm ngầm định được học qua một mạng FFN nhỏ nhận tọa độ thời gian (Positional Encoding) làm đầu vào, giúp tách biệt độ dài bộ lọc khỏi số lượng tham số. |
| 3 | **Matrix decomposition view** | Chỉ ra toán tử Hyena tương đương với việc phân rã một ma trận data-controlled (ma trận mà các phần tử là hàm của đầu vào), tổng quát hóa các kiến trúc đi trước như H3 và GSS. |
| 4 | **SotA on WikiText-103 + The Pile** | Đạt kết quả State-of-the-Art cho các kiến trúc không sử dụng attention (attention-free) ở quy mô dưới 1 tỷ tham số, đạt perplexity tương đương Transformer. |
| 5 | **Long-context efficiency** | Mang lại lợi thế vượt trội về hiệu năng trên chuỗi dài (ví dụ: nhanh hơn 5x so với attention chuẩn và 2x so với FlashAttention ở $L=8192$, nhanh hơn 100x so với FlashAttention ở $L=64K$), mở đường cho mô hình ngữ cảnh cực dài. |

---

## 4. Method — Phương Pháp

### 4.1 Hyena Recurrence
> Toán tử Hyena được định nghĩa thông qua một hệ thức truy hồi lặp lại bậc $N$. Tại mỗi bước truy hồi, giá trị trung gian $z^n$ được tính chập với một bộ lọc dài $h^n$ (tính nhanh qua FFT), sau đó nhân element-wise với một nhánh gating $x^n$ chiếu từ input.

Công thức recurrence:
```
z^(n+1)_t = x^n_t · (h^n * z^n)_t     n = 1,...,N
y_t = z^(N+1)_t
```

Giải thích:
- `z^n`: Tensor trung gian tại bước truy hồi $n$ (bắt đầu bằng $z^1 = v$, là projection cuối cùng của input).
- `x^n`: Projection thứ $n$ của input (đóng vai trò là gate điều phối / gating signal).
- `h^n * z^n`: Phép tích chập dài (long convolution) giữa bộ lọc ngầm định $h^n$ và tensor trung gian $z^n$, được tính nhanh thông qua FFT.
- Complexity: Phép tích chập dài tính bằng FFT có độ phức tạp $O(L \log L)$. Với cấp truy hồi $N$, độ phức tạp tổng thể của toán tử Hyena là $O(N \cdot L \log L)$, subquadratic theo độ dài chuỗi L.

### 4.2 Implicit Filter
> Để giải quyết nhược điểm số lượng tham số tăng tuyến tính theo kích thước bộ lọc trong tích chập dài truyền thống (FIR), Hyena sử dụng bộ lọc ngầm định (Implicit Filter) được tham số hóa thông qua mạng thần kinh FFN nhận Positional Encoding làm đầu vào.

```
h_t = Window(t) · FFN(PositionalEncoding(t))
```

Tại sao dùng implicit:
- **Tách biệt độ dài bộ lọc (filter length) khỏi số lượng tham số (parameter count)**: Số tham số của bộ lọc ngầm định độc lập với độ dài chuỗi L (là O(1) theo L), cho phép học các bộ lọc rất dài (long convolution) mà không làm bùng nổ số lượng tham số.
- **Khả năng biểu diễn mạnh mẽ & kiểm soát độ mịn**: FFN kết hợp với Positional Encoding và hàm suy hao (decay window) có khả năng học các dạng sóng phức tạp (bao gồm các tần số cao ở đầu chuỗi và suy giảm dần về cuối chuỗi), giúp ổn định hóa và cải thiện độ chính xác so với các phương pháp parametrize bộ lọc khác (như SSM, FNO, hay explicit CNN).

---

## 5. Experiments — Kết Quả Bài Gốc

> Kết quả thực nghiệm chính của bài báo gốc:

### WikiText-103
| Model | Perplexity | Params |
|---|---|---|
| Transformer | 18.6 | 125M |
| Hyena-3 | 18.6 | 125M |
| Hyena-3-slim | 18.5 | 125M |
| SotA attention-free trước đó (H3) | 18.5 | 125M |

### The Pile (335M)
| Model | Perplexity (sau 15B tokens) | FLOPs reduction |
|---|---|---|
| Transformer | 9.1 | — |
| Hyena-2 | 9.2 | ~20% (non-parametric FLOPs) |

### Long-context Speedup
| Sequence Length | Speedup vs Attention | Speedup vs FlashAttention |
|---|---|---|
| L = 2,048 | ~1.0x (Crossover point) | < 1.0x (FlashAttention vẫn nhanh hơn) |
| L = 8,192 | 5x | 2x |
| L = 64,000 | > 100x (Attention chuẩn bị OOM) | 100x |

---

## 6. Related Work — Vị Trí Của Hyena

> Mối liên hệ và so sánh giữa Hyena và các kiến trúc liên quan trong landscape:

| Kiến trúc | Năm | Approach | Hyena so sánh thế nào? |
|---|---|---|---|
| Transformer | 2017 | Dense Attention O(L²) | Là baseline chuẩn với cơ chế Attention đầy đủ, độ phức tạp $O(L^2)$ cả về thời gian và bộ nhớ. Hyena thay thế Attention bằng tích chập dài và gating để giảm xuống $O(L \log L)$ mà vẫn giữ được tính chất data-controlled. |
| S4 | 2021 | SSM | Sử dụng State Space Model (SSM) với cấu trúc ma trận HiPPO để học phụ thuộc dài hạn với độ phức tạp $O(L \log L)$ khi huấn luyện và $O(1)$ khi suy luận. Tuy nhiên, S4 thiếu cơ chế nhân cổng phụ thuộc vào dữ liệu (data-controlled gating). |
| H3 | 2022 | SSM + Gating | Kết hợp hai tầng SSM với phép nhân element-wise gating để tạo ra mô hình ngôn ngữ subquadratic hiệu quả. Hyena tổng quát hóa H3 bằng cách tăng cấp độ truy hồi $N > 2$ và thay thế bộ lọc SSM bằng bộ lọc ngầm định FFN linh hoạt hơn. |
| GSS | 2022 | Gated SSM | Sử dụng cơ chế nhân cổng (gating) kết hợp với SSM thu nhỏ chiều dữ liệu để giảm chi phí tính toán. Hyena mở rộng cấu trúc này thành một hệ thống phân cấp gating-convolution lặp lại nhiều lần. |
| Mamba | 2023 | Selective SSM | Giới thiệu cơ chế chọn lọc (selective scan) phụ thuộc vào thời gian và dữ liệu đầu vào trong SSM, đạt hiệu năng rất tốt mà không cần dùng FFT convolution. Mamba ra đời sau và khắc phục điểm yếu về việc không có trạng thái nhận biết nội dung (content-aware decay) của các bộ lọc tích chập tĩnh. |

---

## 7. Nhận Xét Cá Nhân

> Một số góc nhìn cá nhân và phân tích học thuật về bài báo:

**Điểm mạnh của bài báo:**
1. **Thiết kế toán tử subquadratic sáng tạo:** Kết hợp khéo léo tích chập dài qua FFT và nhân cổng đệ quy, chứng minh về mặt toán học và thực nghiệm rằng một mô hình thuần tích chập/truy hồi có thể đạt chất lượng ngôn ngữ tương đương Transformer mà không cần bất kỳ lớp self-attention nào lai vào.
2. **Giải pháp bộ lọc implicit tinh tế:** Việc parametrize bộ lọc bằng mạng FFN nhỏ và Positional Encoding giúp mở rộng bộ lọc lên toàn bộ độ dài chuỗi một cách linh hoạt, độc lập với số lượng tham số, vượt qua hạn chế của CNN truyền thống.

**Điểm hạn chế / cần cải thiện:**
1. **Sự phụ thuộc vào kernel FFT tùy chỉnh:** Hiệu năng thực tế của Hyena phụ thuộc rất lớn vào việc tối ưu hóa kernel FFTConv. Nếu dùng pure Python/PyTorch thuần không có CUDA kernel tối ưu, tốc độ ở độ dài chuỗi ngắn có thể chậm hơn đáng kể so với FlashAttention.
2. **Khả năng hội tụ ở scale nhỏ:** Mô hình có xu hướng hội tụ chậm hơn và yêu cầu điều chỉnh hyperparameter nhạy bén hơn (warmup, learning rate) so với Transformer tiêu chuẩn khi huấn luyện ở các cấu hình nhỏ.

**Điều bất ngờ nhất khi đọc:**
> Khả năng giải quyết tuyệt đối tác vụ Associative Recall ở các chuỗi cực dài (lên tới 131k token) của Hyena mà các mô hình attention-free khác như H3, GSS, hay RWKV đều thất bại hoặc suy giảm nghiêm trọng. Điều này cho thấy tính đúng đắn của việc kết hợp đệ quy đa cấp (hierarchy of recurrence) cùng bộ lọc implicit có độ dài không giới hạn.

---

*File này là output của Thành viên 1, Tuần 1. Cập nhật lần cuối: 11/06/2026*
