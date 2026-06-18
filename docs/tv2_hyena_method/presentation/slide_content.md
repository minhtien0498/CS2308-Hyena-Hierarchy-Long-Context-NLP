# TV2 - Nội Dung Slide 12-22

## Slide 12 - Từ Attention Sang Hyena

**Thông điệp:** Hyena xuất hiện vì cần một operator rẻ hơn Attention nhưng vẫn giữ các tính chất mạnh của Attention.

**Bullet đề xuất:**

- Self-Attention mạnh nhưng chi phí `O(L^2)`.
- Các hướng subquadratic trước đó thường còn capability gap.
- Hyena không xấp xỉ trực tiếp attention matrix.
- Hyena xây operator mới từ long convolution + gating.

**Hình/bảng:** Một mũi tên chuyển ý:

```text
Attention O(L^2) -> cần subquadratic operator -> Hyena
```

## Slide 13 - Ý Tưởng Chính

**Thông điệp:** Hyena gồm hai nguyên thủy: long convolution và gating.

**Bullet đề xuất:**

- Long convolution: lấy thông tin từ toàn bộ sequence.
- Gating: chọn lọc thông tin dựa trên input.
- Kết hợp nhiều bước recurrence tạo thành Hyena hierarchy.

**Hình/bảng:**

```text
Input -> projections -> gates + value
      -> FFTConv -> gate -> FFTConv -> output
```

## Slide 14 - Long Convolution

**Thông điệp:** Long convolution giúp mô hình có global context mà không cần attention matrix.

**Bullet đề xuất:**

- CNN thường dùng kernel ngắn/local.
- Hyena dùng filter dài bằng sequence length `L`.
- Filter dài giúp mô hình hóa phụ thuộc xa.
- Vấn đề: convolution dài cần được tính hiệu quả.

**Hình/bảng:** So sánh local CNN kernel và long filter.

## Slide 15 - Data-Controlled Gating

**Thông điệp:** Gating là thành phần giúp Hyena phụ thuộc vào input.

**Bullet đề xuất:**

- Gate `x^n` được chiếu từ input.
- Gate nhân element-wise với output convolution.
- Nếu convolution là "mang thông tin từ xa", gate là "chọn giữ thông tin nào".
- Đây là điểm giúp Hyena gần attention hơn convolution tĩnh.

**Ví dụ nói:** Với văn bản dài, không phải thông tin xa nào cũng quan trọng; gate học cách tăng/giảm tín hiệu theo nội dung token.

## Slide 16 - Hyena Recurrence

**Thông điệp:** Công thức trung tâm của Hyena.

**Công thức:**

```text
z^(n+1)_t = x^n_t * (h^n * z^n)_t
```

**Giải thích:**

- `z^n`: trạng thái trung gian.
- `h^n * z^n`: long convolution.
- `x^n_t`: gate tại vị trí `t`.
- `N`: số bước recurrence/order.

**Nên nhấn mạnh:** Đây là slide quan trọng nhất của TV2.

## Slide 17 - Order-N Hierarchy

**Thông điệp:** Hyena là một họ toán tử có bậc N, không chỉ một block cố định.

**Bullet đề xuất:**

- N là số lần lặp convolution + gating.
- N lớn hơn -> biểu diễn phức tạp hơn.
- N nhỏ có liên hệ với H3/GSS.
- Trong repo nhóm dùng Hyena-small với `order=2`.

**Liên hệ code:** `models/hyena.py -> HyenaOperator(order=2)`.

## Slide 18 - Matrix View

**Thông điệp:** Hyena có thể nhìn như phân rã có cấu trúc của một ma trận data-controlled.

**Bullet đề xuất:**

- Gating -> diagonal matrix `D_x`.
- Convolution -> Toeplitz matrix `S_h`.
- Hyena xen kẽ `D_x` và `S_h`.
- Không cần materialize ma trận dense `L x L`.

**Cách nói đơn giản:**

> Attention dùng một ma trận lớn; Hyena dùng nhiều ma trận có cấu trúc rẻ hơn để tạo hiệu ứng tương tự.

## Slide 19 - Implicit Filter

**Thông điệp:** Hyena học hàm sinh filter thay vì học trực tiếp filter dài.

**Công thức:**

```text
h_t = Window(t) * FFN(PositionalEncoding(t))
```

**Bullet đề xuất:**

- Explicit filter: lưu vector `h` dài L.
- Implicit filter: FFN sinh `h_t` theo vị trí.
- Số tham số không tăng trực tiếp theo L.
- Window giúp điều chỉnh decay/ổn định filter.

## Slide 20 - FFTConv

**Thông điệp:** FFT giúp tính long convolution hiệu quả.

**Bullet đề xuất:**

- Direct convolution dài có thể tốn kém.
- FFT chuyển convolution thành nhân element-wise trong miền tần số.
- Pipeline: `FFT -> multiply -> iFFT`.
- Complexity: `O(L log L)`.

**Liên hệ code:** `HyenaOperator._causal_fft_conv`.

## Slide 21 - Complexity và Ý Nghĩa

**Thông điệp:** Hyena có lợi thế khi sequence length lớn.

**Bảng đề xuất:**

| Method | Time | Memory |
|---|---|---|
| Standard Attention | `O(L^2)` | `O(L^2)` |
| FlashAttention | `O(L^2)` compute | tối ưu memory access |
| Hyena | `O(N * L log L)` | gần tuyến tính theo L |

**Cần nói rõ:** Ở L nhỏ, Hyena chưa chắc nhanh hơn do overhead FFT.

## Slide 22 - Kết Quả Paper Gốc

**Thông điệp:** Paper cho thấy Hyena thu hẹp khoảng cách với Transformer và nhanh hơn ở long-context.

**Bảng gợi ý:**

| Kết quả | Ý nghĩa |
|---|---|
| WikiText-103 | Hyena đạt chất lượng gần/match Transformer ở scale 125M |
| The Pile 335M | Gần Transformer, giảm khoảng 20% FLOPs |
| Long-context | Nhanh hơn rõ ở L=8K và L=64K |

**Câu bắt buộc:** Đây là kết quả của paper gốc, không phải kết quả nhóm.

