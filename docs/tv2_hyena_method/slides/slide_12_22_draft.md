# TV2 - Draft Slide 12-22

File này là bản nội dung có thể copy sang Google Slides/Canva/Marp. Mỗi slide nên giữ ngắn, ưu tiên hình/bảng.

---

## Slide 12 - Từ Attention Sang Hyena

**Thông điệp:** Cần một operator rẻ hơn Attention nhưng vẫn giữ các tính chất quan trọng.

- Self-Attention mạnh nhưng chi phí `O(L^2)`.
- Các hướng subquadratic trước Hyena vẫn còn capability gap.
- Hyena không xấp xỉ trực tiếp attention matrix.
- Hyena xây operator mới từ **long convolution + gating**.

Visual: `Attention O(L^2) -> Hyena O(N * L log L)`.

---

## Slide 13 - Ý Tưởng Chính

**Hyena = Long Convolution + Data-Controlled Gating**

- Long convolution: mang thông tin từ toàn bộ sequence.
- Gating: chọn lọc thông tin dựa trên input.
- Lặp nhiều bước tạo thành Hyena hierarchy.

Visual:

```text
Input -> Projections -> Gate + Value -> FFTConv -> Gate -> Output
```

---

## Slide 14 - Long Convolution

- CNN thường dùng kernel ngắn, chỉ nhìn local context.
- Hyena dùng filter dài bằng toàn bộ sequence.
- Long convolution giúp mô hình hóa phụ thuộc xa.
- Cần FFTConv để tính hiệu quả.

Visual: local kernel ngắn vs filter dài toàn chuỗi.

---

## Slide 15 - Data-Controlled Gating

- Gate `x^n` được chiếu từ input.
- Gate nhân element-wise với output convolution.
- Convolution mang thông tin xa; gate quyết định giữ/giảm thông tin nào.
- Gating giúp Hyena không phải convolution tĩnh.

Visual: `gate x conv_output`.

---

## Slide 16 - Hyena Recurrence

```text
z^(n+1)_t = x^n_t * (h^n * z^n)_t
```

- `z^n`: trạng thái trung gian.
- `h^n`: long convolution filter.
- `x^n_t`: gate phụ thuộc input.
- `N`: số bước recurrence/order.

Nên nói: đây là công thức trung tâm của phần TV2.

---

## Slide 17 - Order-N Hierarchy

- Hyena có nhiều bậc/order.
- Mỗi bậc thêm một bước convolution + gating.
- N lớn hơn -> operator biểu diễn phức tạp hơn.
- H3/GSS có thể xem là các cấu trúc liên quan ở bậc thấp.

Liên hệ repo: nhóm dùng Hyena-small với `order=2`.

---

## Slide 18 - Matrix View

- Gating tương ứng diagonal matrix `D_x`.
- Convolution tương ứng Toeplitz matrix `S_h`.
- Hyena xen kẽ các ma trận có cấu trúc này.
- Không cần materialize attention matrix dense `L x L`.

Nói đơn giản:

> Attention dùng một ma trận lớn; Hyena dùng phân rã có cấu trúc rẻ hơn.

---

## Slide 19 - Implicit Filter

```text
h_t = Window(t) * FFN(PositionalEncoding(t))
```

- Không học trực tiếp vector filter dài L.
- Học một hàm sinh filter theo vị trí.
- Số tham số không tăng tuyến tính với sequence length.
- Window giúp điều chỉnh decay/ổn định filter.

---

## Slide 20 - FFTConv

```text
h, u -> FFT(h), FFT(u) -> multiply -> iFFT -> h * u
```

- Convolution trong miền thời gian = nhân trong miền tần số.
- FFT giúp tính long convolution trong `O(L log L)`.
- Repo dùng `torch.fft.rfft` trong `models/hyena.py`.

Visual: flow FFTConv.

---

## Slide 21 - Complexity Và Ý Nghĩa

| Method | Time | Memory |
|---|---|---|
| Standard Attention | `O(L^2)` | `O(L^2)` |
| FlashAttention | `O(L^2)` compute | tối ưu memory access |
| Hyena | `O(N * L log L)` | gần tuyến tính theo L |

Lưu ý:

- Hyena mạnh hơn khi L lớn.
- Ở L nhỏ, FFT overhead có thể làm Hyena chưa nhanh hơn.

---

## Slide 22 - Kết Quả Paper Gốc

| Benchmark | Kết quả chính | Ý nghĩa |
|---|---|---|
| Synthetic tasks | Hyena tốt hơn nhiều attention-free operators | Kiểm tra recall/reasoning trên chuỗi dài |
| WikiText-103 | Hyena gần/match Transformer ở scale 125M | Language modeling quality |
| The Pile 335M | Gần Transformer, giảm khoảng 20% FLOPs | Compute efficiency |
| Long-context runtime | 2x ở 8K, 100x ở 64K so với FlashAttention | Lợi thế context dài |

Ghi rõ: **Đây là kết quả paper gốc, không phải kết quả nhóm.**

