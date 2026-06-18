# TV2 - Q&A Hyena Method

## 1. Hyena có phải là attention approximation không?

Không. Hyena không xấp xỉ trực tiếp attention matrix. Nó xây một operator mới từ long convolution và gating, với mục tiêu giữ lại các tính chất quan trọng của attention như data control, context dài và số tham số không phụ thuộc trực tiếp vào độ dài chuỗi.

## 2. Vì sao chỉ convolution là chưa đủ?

Convolution thường dùng filter tương đối tĩnh, không thay đổi nhiều theo nội dung input. Language modeling cần khả năng chọn lọc theo ngữ cảnh. Hyena thêm gating được sinh từ input để output phụ thuộc vào dữ liệu.

## 3. Gating trong Hyena giống attention ở điểm nào?

Không giống hoàn toàn, nhưng cùng có vai trò làm output phụ thuộc vào input. Attention tạo ma trận trọng số từ Q và K; Hyena dùng gate `x^n` chiếu từ input để điều chỉnh output của convolution.

## 4. Long convolution khác CNN thông thường như thế nào?

CNN thông thường dùng kernel ngắn, chỉ nhìn local context. Long convolution dùng filter dài bằng toàn bộ sequence, nên có thể mô hình hóa phụ thuộc xa.

## 5. Vì sao FFTConv có độ phức tạp `O(L log L)`?

FFT tính biến đổi Fourier trong `O(L log L)`. Theo convolution theorem, convolution có thể được tính bằng FFT hai tín hiệu, nhân element-wise trong miền tần số, rồi inverse FFT. Vì vậy chi phí thấp hơn so với xử lý trực tiếp trên chuỗi dài.

## 6. Implicit filter là gì?

Implicit filter là cách sinh filter bằng một hàm học được, thường là FFN nhận positional encoding. Thay vì học trực tiếp vector filter dài L, mô hình học hàm `t -> h_t`.

## 7. Vì sao implicit filter giúp giảm số tham số?

Nếu học trực tiếp filter, filter dài hơn thì cần nhiều tham số hơn. Với implicit filter, số tham số nằm trong FFN, không tăng tuyến tính theo sequence length.

## 8. Hyena có memory `O(L)` thật không?

Về ý tưởng, Hyena không cần lưu ma trận attention `L x L`, nên memory theo sequence length thấp hơn attention. Tuy nhiên memory thực tế còn phụ thuộc implementation, FFT buffer, batch size và hardware.

## 9. Vì sao Hyena có thể chậm ở sequence ngắn?

FFT có overhead. Khi L nhỏ, overhead này có thể lớn hơn lợi ích từ `O(L log L)`. Lợi thế của Hyena rõ hơn ở L lớn và khi có kernel tối ưu.

## 10. Hyena liên hệ gì với H3/GSS?

Paper trình bày Hyena như một họ toán tử tổng quát. Một số mô hình trước như H3/GSS có thể xem là trường hợp bậc thấp hoặc có cấu trúc liên quan đến cách xen kẽ gating và convolution/SSM.

## 11. Matrix view có cần chứng minh khi trình bày không?

Không cần chứng minh chi tiết. Chỉ cần giải thích trực giác: gating là ma trận đường chéo, convolution là ma trận Toeplitz, Hyena là tích xen kẽ các ma trận có cấu trúc này.

## 12. Kết quả paper gốc có phải kết quả nhóm không?

Không. TV2 trình bày kết quả của paper gốc: WikiText-103, The Pile, synthetic tasks, speedup. Kết quả nhóm nằm ở phần TV3 với WikiText-2 và mô hình nhỏ.

## 13. Hyena có tốt hơn Transformer không?

Không nên nói chung chung là tốt hơn. Paper cho thấy Hyena có thể match Transformer trong một số setting và hiệu quả hơn ở long-context. Transformer vẫn rất mạnh và được tối ưu tốt.

## 14. Vì sao Hyena vẫn có unrestricted context?

Vì long convolution dùng filter dài bằng toàn bộ sequence, nên về nguyên tắc thông tin từ xa có thể ảnh hưởng đến output.

## 15. Vì sao paper nói Hyena là attention-free?

Vì Hyena không dùng self-attention layer. Nó thay attention bằng Hyena operator gồm convolution và gating.

