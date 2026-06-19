# TV2 - Study Notes

## 1. Cần Hiểu Gì Trước Khi Làm Slide?

TV2 không cần chứng minh toán học đầy đủ, nhưng cần giải thích được trực giác:

- Attention mạnh vì mỗi token có thể tương tác với nhiều token khác.
- Nhưng attention tạo ma trận `L x L`, nên chi phí tăng theo `O(L^2)`.
- Hyena thay attention bằng một chuỗi phép toán rẻ hơn:
  - Long convolution.
  - Element-wise gating.
  - Implicit filter.
  - FFTConv.

## 2. Hyena Là Gì?

Hyena là một toán tử sequence mixing thay thế attention.

Thay vì:

```text
y = Attention(Q, K, V)
```

Hyena dùng recurrence:

```text
z^(n+1)_t = x^n_t * (h^n * z^n)_t
```

Trong đó:

- `z^n`: trạng thái trung gian.
- `x^n_t`: gate tại vị trí `t`, được chiếu từ input.
- `h^n`: filter dài.
- `h^n * z^n`: long convolution.
- `*` hoặc `·`: nhân element-wise.

## 3. Long Convolution

CNN thông thường dùng kernel ngắn, ví dụ 3, 5, 7 token. Nó chỉ nhìn local context.

Hyena dùng filter dài bằng toàn sequence:

```text
h = [h_0, h_1, ..., h_{L-1}]
```

Nhờ đó mỗi vị trí có thể nhận thông tin từ xa.

Điểm cần nói:

- Long convolution là cách đưa thông tin toàn chuỗi vào mô hình.
- Nó không tạo ma trận attention `L x L`.
- Nếu tính trực tiếp sẽ tốn, nên Hyena dùng FFTConv.

## 4. Gating

Nếu chỉ convolution, filter thường giống nhau cho mọi input. Điều này làm mô hình kém linh hoạt hơn attention.

Hyena thêm gate:

```text
x^n_t * conv_output_t
```

Gate `x^n_t` được sinh từ input nên output phụ thuộc vào dữ liệu. Đây là lý do Hyena vẫn có tính **data-controlled**.

Cách giải thích dễ:

> Long convolution mang thông tin từ xa về; gating quyết định tại mỗi vị trí nên giữ hay giảm thông tin nào dựa trên nội dung input.

## 5. Implicit Filter

Nếu học trực tiếp filter dài L, số tham số sẽ tăng theo L. Ví dụ L càng dài thì vector `h` càng dài.

Hyena không lưu trực tiếp toàn bộ filter như tham số. Thay vào đó, nó học một hàm sinh filter:

```text
h_t = Window(t) * FFN(PositionalEncoding(t))
```

Ý nghĩa:

- `t`: vị trí trong sequence.
- `PositionalEncoding(t)`: mã hóa vị trí.
- `FFN(...)`: mạng nhỏ sinh giá trị filter.
- `Window(t)`: điều chỉnh decay/độ suy giảm theo thời gian.

Nói đơn giản:

> Thay vì học từng điểm của filter, Hyena học một công thức để sinh ra filter.

## 6. FFTConv

Convolution trực tiếp trên chuỗi dài có thể tốn kém. FFT dựa trên convolution theorem:

```text
convolution trong miền thời gian
= nhân element-wise trong miền tần số
```

Pipeline:

```text
h, u
-> FFT(h), FFT(u)
-> nhân element-wise
-> iFFT
-> output convolution
```

Trong code repo, xem:

```text
models/hyena.py -> HyenaOperator._causal_fft_conv
```

Code dùng:

```python
H = torch.fft.rfft(h, n=fft_len, dim=-1)
V = torch.fft.rfft(v, n=fft_len, dim=-1)
Y = H * V
y = torch.fft.irfft(Y, n=fft_len, dim=-1)[..., :L]
```

## 7. Complexity

So sánh chính:

| Toán tử | Time | Ý nghĩa |
|---|---|---|
| Attention | `O(L^2)` | Tạo/tính tương tác mọi cặp token |
| Hyena | `O(N * L log L)` | N bước recurrence, mỗi bước dùng FFTConv |

Với L nhỏ, Hyena có thể chưa nhanh do overhead FFT. Với L lớn, `L log L` tăng chậm hơn `L^2`.

## 8. Matrix View

Đây là phần khó nhất. Không cần chứng minh sâu.

Chỉ cần nói:

- Gating có thể xem như ma trận đường chéo `D_x`.
- Convolution có thể xem như ma trận Toeplitz `S_h`.
- Hyena là tích xen kẽ:

```text
D_x * S_h * D_x * S_h * ...
```

Ý nghĩa:

> Attention dùng một ma trận dense data-controlled. Hyena không tạo ma trận dense đó, mà dùng một phân rã có cấu trúc rẻ hơn nhưng vẫn phụ thuộc dữ liệu.

## 9. Kết Quả Paper Gốc

Các số nên nhớ:

- WikiText-103: Hyena đạt perplexity gần/match Transformer ở quy mô 125M.
- The Pile: Hyena-2 ở 335M parameters gần Transformer, với giảm FLOPs khoảng 20%.
- Long-context speedup:
  - Khoảng 5x so với attention chuẩn ở L=8192.
  - Khoảng 2x so với FlashAttention ở L=8192.
  - Khoảng 100x so với FlashAttention ở L=64K.

Lưu ý khi nói:

> Đây là kết quả của paper gốc, không phải kết quả reproduction của nhóm.

