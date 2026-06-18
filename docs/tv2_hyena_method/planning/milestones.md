# TV2 - Recap, Milestones và Sync-Up Plan

File này dùng để theo dõi tiến độ phần **TV2: Hyena Method & Paper Results**. Mục tiêu là mọi người có thể làm riêng trước, sau đó có một buổi call để ráp mạch và kiểm tra phần TV2 có nối tốt với TV1/TV3 không.

---

## 1. Recap Nhanh Phần TV2

TV2 phụ trách **slide 12-22**, khoảng **15 phút nói**.

Mạch kể chính:

```text
TV1 đã chỉ ra Attention mạnh nhưng bị O(L^2)
-> TV2 giới thiệu Hyena như một operator thay thế attention
-> Hyena = long convolution + data-controlled gating
-> Implicit filter giúp filter dài nhưng ít tham số
-> FFTConv giúp tính long convolution trong O(L log L)
-> Paper gốc cho thấy Hyena match Transformer ở một số benchmark và nhanh hơn ở long-context
-> TV3 tiếp tục với reproduction quy mô nhỏ của nhóm
```

Thông điệp cần giữ:

> Hyena không xấp xỉ trực tiếp attention matrix. Hyena xây một toán tử mới, dùng long convolution để nhìn xa và gating để phụ thuộc vào input, nhờ đó đạt chi phí dưới bậc hai khi sequence length lớn.

---

## 2. Output Cần Hoàn Thành

| Output | File hỗ trợ | Người phụ trách chính |
|---|---|---|
| Nội dung slide 12-22 | `slide_content.md` | TV2 |
| Lời nói/speaker notes | `speaker_notes.md` | TV2 |
| Q&A phần Hyena method | `qna_tv2.md` | TV2 |
| Hình/bảng cần chuẩn bị | `visual_checklist.md` | TV2 |
| Kiến thức nền cần học | `study_notes.md` | TV2 |
| Câu chuyển TV1 -> TV2 và TV2 -> TV3 | `README.md` | TV2 phối hợp TV1/TV3 |

---

## 3. Milestone và Deadline Đề Xuất

Mốc dưới đây dùng dạng **T+N ngày**, trong đó **T0 là ngày nhóm chốt phân công**. Nếu nhóm bắt đầu ngay ngày 14/06/2026 thì có thể dùng cột ngày gợi ý.

| Milestone | Deadline tương đối | Nếu T0 = 14/06/2026 | Output cần có | Tiêu chí hoàn thành |
|---|---:|---:|---|---|
| M1 - Đọc hiểu phần TV2 | T+2 | 16/06/2026 | Đọc xong `study_notes.md`, `paper_summary.md` Section Method/Experiments | TV2 giải thích miệng được long convolution, gating, implicit filter, FFTConv |
| M2 - Chốt nội dung slide | T+4 | 18/06/2026 | Draft bullet cho slide 12-22 | Mỗi slide có 1 thông điệp chính, không quá 4 bullet |
| M3 - Chốt visual | T+6 | 20/06/2026 | Hình/bảng cho slide 12-22 | Có đủ sơ đồ Hyena, recurrence, FFTConv, complexity table, paper results table |
| M4 - Viết speaker notes | T+8 | 22/06/2026 | Notes nói 15 phút | Nói thử không cần nhìn quá nhiều vào slide |
| M5 - Chuẩn bị Q&A | T+9 | 23/06/2026 | Ít nhất 5-10 câu Q&A phần TV2 | Trả lời được các câu về recurrence, gating, FFTConv, implicit filter |
| M6 - Call sync-up lần 1 | T+10 hoặc T+11 | 24-25/06/2026 | Call nhóm 45-60 phút | TV1/TV2/TV3 ráp mạch, sửa chỗ lặp hoặc bị hở ý |
| M7 - Chốt bản gần final | T+14 | 28/06/2026 | Slide + notes TV2 gần final | TV2 nói thử trong 15 phút, không quá giờ |
| M8 - Tổng duyệt | T+18 đến T+20 | 02-04/07/2026 | Full deck + Q&A | Cả nhóm chạy thử 45 phút + hỏi đáp |

Nếu lịch nhóm khác, chỉ cần giữ thứ tự milestone, không bắt buộc đúng ngày gợi ý.

---

## 4. Agenda Buổi Call Sync-Up

Thời lượng đề xuất: **45-60 phút**.

| Phần | Thời lượng | Nội dung |
|---|---:|---|
| 1. Check mạch tổng thể | 5 phút | TV1 -> TV2 -> TV3 đã nối logic chưa |
| 2. TV1 nói nhanh phần trước TV2 | 5 phút | TV1 nói phần kết thúc slide 11 để TV2 biết câu chuyển |
| 3. TV2 trình bày thử slide 12-22 | 15 phút | Nói như khi present thật, các bạn ghi lỗi/ý chưa rõ |
| 4. Feedback cho TV2 | 10 phút | Slide nào dài, slide nào khó hiểu, visual nào thiếu |
| 5. TV3 nối từ TV2 sang reproduction | 5 phút | Kiểm tra câu chuyển từ paper results sang small-scale reproduction |
| 6. Q&A thử | 10-15 phút | Mỗi người hỏi TV2 2-3 câu khó |
| 7. Chốt việc sau call | 5 phút | Ai sửa slide nào, deadline sửa |

---

## 5. Checklist Trước Khi Call

TV2 nên chuẩn bị trước:

- [ ] Đã đọc `study_notes.md`.
- [ ] Đã có bullet cho slide 12-22.
- [ ] Đã chọn visual cho từng slide theo `visual_checklist.md`.
- [ ] Đã đọc speaker notes ít nhất 1 lần.
- [ ] Đã chuẩn bị 5 câu Q&A quan trọng nhất.
- [ ] Đã ghi rõ slide 22 là **kết quả paper gốc**, không phải kết quả nhóm.

TV1 cần chuẩn bị:

- [ ] Câu chuyển từ slide 11 sang slide 12.
- [ ] Nhắc lại 3 tính chất của Attention để TV2 dùng tiếp.

TV3 cần chuẩn bị:

- [ ] Câu chuyển từ slide 22 sang slide 23.
- [ ] Scope reproduction để không lẫn với kết quả paper gốc.

---

## 6. Rủi Ro Cần Tránh

| Rủi ro | Cách xử lý |
|---|---|
| Slide 18 matrix view quá khó | Chỉ giải thích trực giác: diagonal = gating, Toeplitz = convolution |
| Slide 20 FFTConv quá toán | Dùng flow `FFT -> multiply -> iFFT`, không chứng minh sâu |
| Nói Hyena "tốt hơn Transformer" quá mạnh | Đổi thành: Hyena match Transformer trong một số setting và hiệu quả hơn ở long-context |
| Lẫn kết quả paper với kết quả nhóm | Slide 22 ghi rõ "Paper gốc"; TV3 mới nói kết quả nhóm |
| Quá giờ 15 phút | Slide 18 và 20 nói ngắn, tập trung trực giác |

