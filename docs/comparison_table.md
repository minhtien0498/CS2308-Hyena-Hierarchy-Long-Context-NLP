# Bảng So Sánh Transformer vs Hyena Hierarchy
**Phụ trách:** Thành viên 1 (TV1) | **Deadline:** Cuối Tuần 1

---

Bản so sánh chi tiết các khía cạnh kiến trúc, độ phức tạp thuật toán và hiệu năng thực nghiệm giữa mô hình **Transformer (Self-Attention)** và **Hyena Hierarchy**:

| Tiêu Chí So Sánh | Transformer (Self-Attention) | Hyena Hierarchy |
| :--- | :--- | :--- |
| **Phép toán cốt lõi (Core Operation)** | **Scaled Dot-Product Attention**:<br>Tính toán ma trận tương quan đầy đủ giữa Query, Key và Value.<br>`Attention(Q,K,V) = softmax(Q·Kᵀ / √d_k) · V` | **Long Convolution + Element-wise Gating**:<br>Hệ thức truy hồi bậc $N$ xen kẽ phép tích chập dài và phép nhân chập cổng đầu vào.<br>`z^(n+1)_t = x^n_t · (h^n * z^n)_t` |
| **Độ phức tạp thời gian (Time Complexity)** | **$O(L^2 \cdot d)$** per layer.<br>Tăng theo hàm bậc hai của chiều dài chuỗi $L$. | **$O(N \cdot L \log L)$** per layer.<br>Tăng tiệm cận tuyến tính nhờ phép tích chập qua FFT. |
| **Độ phức tạp bộ nhớ (Space Complexity)** | **$O(L^2)$** per layer.<br>Do phải lưu trữ ma trận attention $L \times L$ để tính toán đạo hàm. | **$O(L)$** per layer.<br>Chỉ cần lưu trữ các giá trị trung gian và bộ lọc ngầm định, không cần ma trận ô vuông. |
| **Tính phụ thuộc dữ liệu (Data-Controlled)** | **Có (Đầy đủ)**.<br>Ma trận attention $A$ phụ thuộc trực tiếp vào mối tương quan động giữa các tokens đầu vào ($Q$ và $K$). | **Có (Độ phức tạp thấp)**.<br>Đầu ra được điều tiết (gated) động qua các nhánh chiếu $x^n$ phụ thuộc vào input. |
| **Khả năng song song hóa (Parallelization)** | **Tốt**.<br>Tất cả các token có thể tính toán attention đồng thời (phù hợp GPU). | **Tốt**.<br>Nhờ toán tử FFT, các phép tích chập dài có thể song song hóa hoàn toàn trong pha huấn luyện. |
| **Khuynh hướng hội tụ (Convergence)** | **Nhanh và ổn định**.<br>Rất tốt ở cả các cấu hình mô hình nhỏ và lớn nhờ cơ chế liên kết trực tiếp giữa các vị trí. | **Hơi chậm hơn ở quy mô nhỏ**.<br>Đòi hỏi cấu hình hyperparameters (warmup, learning rate) nhạy bén hơn, đạt hiệu năng tối ưu ở quy mô lớn. |
| **Độ dài ngữ cảnh tối đa (Max Context)** | **Bị giới hạn**.<br>Thường bị Out-of-Memory (OOM) ở $L > 8192$ (hoặc lớn hơn một chút nếu dùng FlashAttention). | **Không giới hạn (Unbounded)**.<br>Hoạt động ổn định trên các chuỗi cực dài (lên tới $100K+$ tokens) trên phần cứng tiêu chuẩn. |
| **Khả năng suy luận tuần tự (Inference)** | **$O(L)$ per step** (hoặc $O(1)$ nếu dùng KV Cache).<br>KV cache tiêu tốn bộ nhớ rất lớn khi chuỗi dài. | **$O(1)$ per step** (hoạt động như mô hình Recurrent/SSM tuần tự).<br>Bộ nhớ suy luận ổn định và cực kỳ tiết kiệm. |
| **Độ chín muồi kỹ thuật (Implementation)** | **Rất cao**.<br>Có nhiều thư viện được tối ưu sâu ở cấp độ phần cứng (như FlashAttention, vLLM, TensorRT). | **Trung bình**.<br>Đòi hỏi thư viện FFTConv tối ưu hoặc custom CUDA kernels để đạt được hiệu năng lý thuyết tối đa. |

---

### Phân Tích Chi Tiết Các Khía Cạnh Quan Trọng

#### 1. Tại sao Hyena có thể vượt qua bottleneck $O(L^2)$?
Transformer bắt buộc phải thực hiện nhân ma trận giữa $Q$ (Query) kích thước $[L \times d]$ và $K^T$ (Key) kích thước $[d \times L]$, tạo ra một ma trận có kích thước $[L \times L]$. Điều này đồng nghĩa với việc mọi token đều có thể tương tác trực tiếp với bất kỳ token nào khác. 

Hyena giải quyết vấn đề này bằng cách chuyển đổi toán tử kết hợp thông tin sang **miền tần số** bằng thuật toán Fast Fourier Transform (FFT). Phép tích chập trong miền thời gian:
$$ y_t = (h * u)_t = \sum_{\tau} h_{t-\tau} u_{\tau} $$
sẽ tương đương phép nhân element-wise trong miền tần số:
$$ \mathcal{F}(y) = \mathcal{F}(h) \cdot \mathcal{F}(u) $$
Độ phức tạp của thuật toán FFT chỉ là $O(L \log L)$, từ đó đưa tổng chi phí tính toán của tích chập dài xuống dưới bậc hai.

#### 2. Vấn đề "Data Control"
Một trong những lý do khiến các kiến trúc tích chập truyền thống (CNN) thất bại trong việc thay thế Transformer trên các tác vụ ngôn ngữ lớn là do các bộ lọc tích chập là **tĩnh** (không thay đổi theo nội dung của chuỗi đầu vào). 

Hyena giải quyết điều này bằng cách sử dụng cấu trúc **gating (nhân chập cổng)** đa cấp. Đầu vào $u$ được chiếu thành $N+1$ nhánh: $v, x^1, x^2, ..., x^N$. Các nhánh $x^n$ đóng vai trò điều khiển độ mở của cổng tại mỗi bước đệ quy, làm thay đổi trực tiếp kết quả tích chập dựa trên ngữ cảnh thực tế của dữ liệu. Điều này mang lại khả năng "data control" tương đương với Attention nhưng có chi phí rẻ hơn nhiều.

---
*File này là output của Thành viên 1, Tuần 1. Cập nhật lần cuối: 11/06/2026*
