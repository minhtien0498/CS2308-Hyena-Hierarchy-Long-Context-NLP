# TV2 - Speaker Notes Gợi Ý

Mục tiêu thời gian: **15 phút cho 11 slide**.  
Mỗi slide nên nói khoảng 60-90 giây. Slide 16, 19, 20, 21 có thể nói lâu hơn một chút.

---

## Slide 12 - Từ Attention Sang Hyena

"Ở phần trước, chúng ta đã thấy Self-Attention rất mạnh nhưng bị giới hạn bởi chi phí `O(L^2)`. Vấn đề đặt ra là: liệu có thể giữ lại những tính chất quan trọng của Attention, nhưng dùng một toán tử rẻ hơn không? Hyena trả lời câu hỏi này bằng cách không xấp xỉ trực tiếp attention matrix, mà xây một operator mới từ hai primitive: long convolution và gating."

## Slide 13 - Ý Tưởng Chính

"Ý tưởng chính của Hyena có thể tóm gọn là long convolution cộng với gating. Long convolution giúp mô hình nhận thông tin từ toàn bộ sequence, tức là vẫn có global context. Gating giúp mô hình chọn lọc thông tin dựa trên input, để operator không bị tĩnh như convolution thông thường. Khi lặp hai bước này nhiều lần, ta có Hyena hierarchy."

## Slide 14 - Long Convolution

"CNN truyền thống thường dùng kernel ngắn, ví dụ chỉ nhìn vài token lân cận. Điều này tốt cho local pattern nhưng không đủ cho phụ thuộc xa. Hyena dùng filter dài bằng toàn bộ sequence. Nhờ vậy một token có thể nhận thông tin từ rất xa. Tuy nhiên, nếu tính convolution dài một cách trực tiếp thì chi phí vẫn lớn, nên phần sau Hyena dùng FFT để tính nhanh."

## Slide 15 - Data-Controlled Gating

"Nếu chỉ dùng convolution thì filter gần như cố định, không linh hoạt theo từng input. Đây là lý do các mô hình convolution thuần thường khó thay thế Attention trong language modeling. Hyena thêm gating: các gate được chiếu từ input và nhân trực tiếp với output của convolution. Nhờ vậy, mô hình có thể quyết định thông tin nào nên được giữ lại hoặc giảm đi tùy theo nội dung chuỗi."

## Slide 16 - Hyena Recurrence

"Đây là công thức trung tâm của Hyena. Ở bước thứ n, ta lấy trạng thái trung gian `z^n`, cho đi qua long convolution với filter `h^n`, sau đó nhân với gate `x^n`. Kết quả là `z^(n+1)`. Nếu lặp N lần, ta có Hyena order N. Trong công thức này, convolution đóng vai trò mang thông tin dài hạn, còn gate đóng vai trò điều khiển theo dữ liệu."

## Slide 17 - Order-N Hierarchy

"Từ 'hierarchy' trong Hyena đến từ việc operator có thể có nhiều bậc. N là số lần lặp lại convolution và gating. Khi N tăng, operator có khả năng biểu diễn phức tạp hơn. Paper cũng chỉ ra rằng một số mô hình trước như H3 hoặc GSS có thể xem như trường hợp bậc thấp hoặc có cấu trúc liên quan. Trong reproduction của nhóm, ta dùng cấu hình nhỏ với order bằng 2."

## Slide 18 - Matrix View

"Phần này có thể nhìn hơi toán học, nhưng trực giác khá đơn giản. Gating tương ứng với một ma trận đường chéo, vì nó nhân từng vị trí hoặc từng channel. Convolution tương ứng với một ma trận Toeplitz, vì cùng một filter được trượt qua chuỗi. Hyena xen kẽ các ma trận đường chéo và Toeplitz. Vì vậy, thay vì tạo một ma trận attention dense kích thước `L x L`, Hyena dùng một phân rã có cấu trúc rẻ hơn nhưng vẫn phụ thuộc dữ liệu."

## Slide 19 - Implicit Filter

"Một vấn đề của long convolution là filter dài bằng sequence. Nếu học trực tiếp toàn bộ vector filter thì số tham số sẽ tăng theo L. Hyena giải quyết bằng implicit filter: thay vì lưu từng giá trị của filter, mô hình học một hàm nhỏ, cụ thể là FFN nhận positional encoding của vị trí t, rồi sinh ra giá trị `h_t`. Có thể hiểu là học công thức sinh filter thay vì học từng điểm trong filter."

## Slide 20 - FFTConv

"Để tính long convolution hiệu quả, Hyena dùng FFT. Theo convolution theorem, convolution trong miền thời gian tương đương với phép nhân element-wise trong miền tần số. Vì vậy ta lấy FFT của filter và input, nhân chúng lại, rồi dùng inverse FFT để quay về miền thời gian. Chi phí giảm xuống `O(L log L)`. Trong code của nhóm, phần này nằm trong hàm `_causal_fft_conv` của `models/hyena.py`."

## Slide 21 - Complexity và Ý Nghĩa

"So với Attention chuẩn có chi phí `O(L^2)`, Hyena có chi phí khoảng `O(N * L log L)`, với N là order của recurrence. Khi L lớn, `L log L` tăng chậm hơn nhiều so với `L^2`. Đây là lý do Hyena đặc biệt phù hợp với long-context. Tuy nhiên, ở sequence ngắn, Hyena có thể chưa nhanh hơn vì FFT có overhead và implementation trong repo là PyTorch thuần, không phải CUDA kernel tối ưu như paper."

## Slide 22 - Kết Quả Paper Gốc

"Paper đánh giá Hyena trên nhiều nhóm thí nghiệm. Với các synthetic tasks như recall và reasoning trên chuỗi dài, Hyena cải thiện rõ so với nhiều mô hình attention-free trước đó. Trên WikiText-103 và The Pile, Hyena đạt chất lượng gần hoặc match Transformer trong một số setting, đồng thời giảm FLOPs. Về long-context runtime, Hyena nhanh hơn rõ khi sequence length lớn, ví dụ ở 8K và 64K tokens. Cần nhấn mạnh đây là kết quả của paper gốc; phần reproduction của nhóm sẽ được trình bày sau."

