# TV2 - Visual Checklist

## Hình/Bảng Nên Có Cho Slide 12-22

| Slide | Visual cần có | Có thể làm bằng |
|---:|---|---|
| 12 | Sơ đồ chuyển từ Attention sang Hyena | Mũi tên đơn giản |
| 13 | Tổng quan Hyena = convolution + gating | Flow diagram |
| 14 | Local CNN kernel vs long convolution filter | Hình 1D sequence |
| 15 | Gate điều chỉnh output convolution | Sơ đồ nhân element-wise |
| 16 | Hyena recurrence | Công thức lớn + chú thích |
| 17 | Order-N hierarchy | Stack nhiều block conv+gate |
| 18 | Matrix view | Diagonal matrix + Toeplitz matrix |
| 19 | Implicit filter | `PE(t) -> FFN -> h_t`, kèm decay window |
| 20 | FFTConv | `FFT(h), FFT(u) -> multiply -> iFFT` |
| 21 | Complexity table | Bảng Attention vs FlashAttention vs Hyena |
| 22 | Paper results table | Bảng WikiText-103/The Pile/speedup |

## Gợi Ý Thiết Kế Nhanh

- Dùng màu xanh cho Transformer/Attention.
- Dùng màu đỏ/cam cho Hyena.
- Các slide công thức chỉ nên có 1 công thức chính.
- Không đưa quá 4 bullet trên một slide.
- Slide 18 matrix view không cần quá toán học; ưu tiên trực giác.

## Bảng Kết Quả Paper Gốc Gợi Ý

| Benchmark | Kết quả chính | Ý nghĩa |
|---|---|---|
| Synthetic recall/reasoning | Hyena vượt nhiều attention-free operators | Kiểm tra khả năng nhớ và suy luận trên chuỗi dài |
| WikiText-103 | Hyena match/gần Transformer ở scale 125M | Chất lượng language modeling tốt |
| The Pile 335M | Gần Transformer, giảm khoảng 20% FLOPs | Hiệu quả compute tốt hơn |
| Runtime long-context | 2x vs FlashAttention ở 8K, 100x ở 64K | Lợi thế khi context rất dài |

## Cảnh Báo Khi Làm Visual

- Không ghi kết quả paper gốc như kết quả nhóm.
- Không nói Hyena luôn nhanh hơn Transformer ở mọi L.
- Không để slide 16, 18, 19, 20 quá nhiều chữ vì đây là các slide khó.
- Nếu lấy hình từ paper, cần ghi nguồn: Poli et al., ICML 2023.

