# TV2 - Checklist Công Việc Cần Hoàn Thành

Mục tiêu: hoàn thành toàn bộ phần **slide 12-22** sao cho có thể trình bày độc lập trong khoảng **15 phút**, đồng thời nối mạch tốt với TV1 và TV3.

---

## 1. Checklist Theo Output

| Nhóm việc | Output cần có | Trạng thái |
|---|---|---|
| Đọc hiểu | Nắm được long convolution, gating, recurrence, implicit filter, FFTConv | [ ] |
| Slide content | Bullet hoàn chỉnh cho slide 12-22 | [ ] |
| Visual | Hình/bảng cho từng slide khó | [ ] |
| Speaker notes | Lời nói 15 phút cho slide 12-22 | [ ] |
| Q&A | Ít nhất 5-10 câu hỏi đáp phần method | [ ] |
| Handoff | Câu chuyển TV1 -> TV2 và TV2 -> TV3 | [ ] |
| Review | Nhờ ít nhất 1 bạn nghe thử phần TV2 | [ ] |

---

## 2. Checklist Theo Slide

| Slide | Cần hoàn thành | Trạng thái |
|---:|---|---|
| 12 | Câu chuyển từ Attention sang Hyena | [ ] |
| 13 | Sơ đồ ý tưởng Hyena = long convolution + gating | [ ] |
| 14 | So sánh long convolution với CNN local | [ ] |
| 15 | Giải thích gating và data-controlled | [ ] |
| 16 | Công thức Hyena recurrence, giải thích từng biến | [ ] |
| 17 | Ý nghĩa order-N hierarchy, liên hệ H3/GSS | [ ] |
| 18 | Matrix view: diagonal + Toeplitz, nói trực giác | [ ] |
| 19 | Implicit filter: công thức `h_t = Window(t) * FFN(PE(t))` | [ ] |
| 20 | FFTConv: flow `FFT -> multiply -> iFFT` | [ ] |
| 21 | Bảng complexity Attention vs FlashAttention vs Hyena | [ ] |
| 22 | Bảng kết quả paper gốc, tách khỏi kết quả nhóm | [ ] |

---

## 3. Ưu Tiên Khi Không Đủ Thời Gian

Nếu thời gian ít, ưu tiên theo thứ tự:

1. Slide 16 - Hyena recurrence.
2. Slide 20 - FFTConv.
3. Slide 21 - Complexity.
4. Slide 22 - Paper results.
5. Slide 18 - Matrix view chỉ nói trực giác, không đào sâu.

Các slide dễ có thể làm gọn:

- Slide 12.
- Slide 13.
- Slide 14.
- Slide 15.

---

## 4. Tiêu Chí Hoàn Thành

Phần TV2 được xem là ổn nếu:

- Nói được trong 15 phút, không quá 17 phút.
- Người nghe hiểu được Hyena gồm convolution + gating.
- Giải thích được vì sao dùng FFT giúp giảm complexity.
- Không nhầm kết quả paper gốc với kết quả nhóm.
- Trả lời được câu hỏi: "Hyena có phải attention approximation không?"

