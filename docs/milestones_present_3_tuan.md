# Milestones Chung Cho Nhóm - Present Hyena Hierarchy

**Bài báo:** *Hyena Hierarchy: Towards Larger Convolutional Language Models* - Poli et al., ICML 2023  
**Thời lượng:** 45 phút trình bày + 15 phút hỏi đáp  
**Cấu trúc:** 33 slide, 3 thành viên, mỗi người khoảng 11 slide / 15 phút  
**Mục tiêu:** Mỗi thành viên làm phần riêng nhưng phải ráp được thành một mạch thống nhất.

---

## 1. Recap Mạch Trình Bày Của Cả Nhóm

Mạch kể chung:

```text
TV1: Transformer mạnh nhưng Self-Attention bị O(L^2)
-> TV2: Hyena thay Attention bằng long convolution + gating + FFTConv
-> TV2: Paper gốc cho thấy Hyena match Transformer trong một số benchmark và nhanh hơn ở long-context
-> TV3: Nhóm tái hiện quy mô nhỏ trên WikiText-2 để kiểm chứng xu hướng
-> Cả nhóm: Q&A, trả lời theo phần phụ trách
```

Thông điệp chung:

> Hyena cho thấy attention không phải con đường duy nhất để xây dựng mô hình ngôn ngữ long-context. Bài báo đề xuất một operator attention-free có chi phí dưới bậc hai, còn nhóm thực hiện small-scale reproduction để hiểu và kiểm chứng xu hướng trong phạm vi môn học.

---

## 2. Phân Công Tổng Quan

| Thành viên | Slide | Vai trò | Output chính |
|---|---:|---|---|
| TV1 | 1-11 | Nền tảng, motivation, Self-Attention, related work | Slide nền tảng, bảng related work, Q&A lý thuyết |
| TV2 | 12-22 | Hyena method và kết quả paper gốc | Slide method, sơ đồ Hyena, speaker notes, Q&A method |
| TV3 | 23-33 | Reproduction, kết quả nhóm, thảo luận | Slide thực nghiệm, bảng/plot kết quả, Q&A reproduction |

Phần hỏi đáp:

| Nhóm câu hỏi | Người trả lời chính | Người bổ sung |
|---|---|---|
| Transformer, Self-Attention, `O(L^2)`, related work | TV1 | TV2 |
| Hyena operator, FFTConv, gating, paper results | TV2 | TV1 |
| Dataset, code, reproduction, kết quả nhóm | TV3 | TV2 |
| Giới hạn, phản biện, scope nhóm | Người gần phần câu hỏi nhất | Cả nhóm |

---

## 3. Milestone Và Deadline Đề Xuất

Mốc dưới đây dùng dạng **T+N ngày**, trong đó **T0 là ngày nhóm chốt phân công**. Nếu nhóm bắt đầu ngay **14/06/2026**, có thể dùng cột ngày gợi ý.

### 3.1 Bảng Deadline Tổng Quan Theo Tuần

| Tuần | Mốc | Deadline gợi ý | Mục tiêu chính | Output cần có |
|---|---|---|---|---|
| Tuần 1 | M1.1 | 16/06/2026 | Đọc hiểu và chốt mạch từng phần | Mỗi người nắm phần mình; thống nhất mạch TV1 -> TV2 -> TV3 |
| Tuần 1 | M1.2 | 20/06/2026 | Chốt bullet và visual thô | Mỗi người có bullet 11 slide; có bảng/hình/công thức chính |
| Tuần 2 | M2.1 | 23/06/2026 | Chốt số liệu/speaker notes bản đầu | Có E1/E2/E3 hoặc preliminary result; mỗi người có speaker notes bản nháp |
| Tuần 2 | M2.2 | 26/06/2026 | Call sync-up và Q&A bản đầu | Call ráp mạch; mỗi người có ít nhất 5 câu Q&A |
| Tuần 3 | M3.1 | 01/07/2026 | Tổng duyệt lần 1 | Slide gần final; chạy thử 45 phút; ghi lại phần quá giờ/chưa rõ |
| Tuần 3 | M3.2 | 04/07/2026 | Chốt bản cuối | Slide final; Q&A final; backup PDF/source/code |

### 3.2 Milestone Chi Tiết

| Milestone | Deadline tương đối | Nếu T0 = 14/06/2026 | Output cần có | Ai chịu trách nhiệm |
|---|---:|---:|---|---|
| M1 - Chốt scope và chia phần | T+0 | 14/06/2026 | Chốt 33 slide, mỗi người 11 slide | Cả nhóm |
| M2 - Đọc hiểu phần được giao | T+2 | 16/06/2026 | Mỗi người nắm được mạch phần mình | TV1, TV2, TV3 |
| M3 - Draft bullet slide | T+4 | 18/06/2026 | Bullet thô cho slide 1-33 | Mỗi người làm 11 slide của mình |
| M4 - Chốt visual/bảng/công thức | T+6 | 20/06/2026 | Hình, bảng, công thức chính cho từng phần | Cả nhóm |
| M5 - Chạy/chốt thực nghiệm tối thiểu | T+8 | 22/06/2026 | E1/E2/E3 hoặc preliminary result rõ ràng | TV3 chính, TV1/TV2 hỗ trợ |
| M6 - Viết speaker notes | T+9 | 23/06/2026 | Notes nói khoảng 15 phút/người | Mỗi thành viên |
| M7 - Chuẩn bị Q&A theo phần | T+10 | 24/06/2026 | Mỗi người ít nhất 5 câu Q&A | Mỗi thành viên |
| M8 - Call sync-up lần 1 | T+11 hoặc T+12 | 25-26/06/2026 | Ráp mạch TV1 -> TV2 -> TV3, phát hiện nghẽn | Cả nhóm |
| M9 - Sửa sau sync-up | T+14 | 28/06/2026 | Slide gần final, số liệu rõ ràng | Cả nhóm |
| M10 - Tổng duyệt lần 1 | T+17 | 01/07/2026 | Chạy thử 45 phút, đo thời gian từng người | Cả nhóm |
| M11 - Tổng duyệt cuối | T+19 hoặc T+20 | 03-04/07/2026 | Slide final, Q&A final, backup file | Cả nhóm |

Nếu lịch nhóm khác, chỉ cần giữ thứ tự milestone. Quan trọng nhất là **M5 thực nghiệm** và **M8 call sync-up** không nên để quá sát ngày trình bày.

---

## 4. Output Theo Từng Thành Viên

### TV1 - Nền Tảng Và Motivation

| Output | File tham khảo | Deadline gợi ý |
|---|---|---|
| Bullet slide 1-11 | `slides/slide_outline.md`, `docs/theory_attention.md` | M3 |
| Bảng related work | `docs/related_work_notes.md`, `docs/comparison_table.md` | M4 |
| Speaker notes 15 phút | tự viết theo slide 1-11 | M6 |
| Q&A lý thuyết | phần Q&A trong `docs/phan_cong_present_hyena_3_tuan.md` | M7 |

### TV2 - Hyena Method Và Paper Results

| Output | File tham khảo | Deadline gợi ý |
|---|---|---|
| Bullet slide 12-22 | `slides/slide_outline.md`, `docs/paper_summary.md` | M3 |
| Sơ đồ Hyena/FFTConv/complexity | `docs/comparison_table.md`, `models/hyena.py` | M4 |
| Speaker notes 15 phút | tự viết theo slide 12-22 | M6 |
| Q&A method | phần Q&A trong `docs/phan_cong_present_hyena_3_tuan.md` | M7 |

### TV3 - Reproduction Và Kết Quả Nhóm

| Output | File tham khảo | Deadline gợi ý |
|---|---|---|
| Bullet slide 23-33 | `slides/slide_outline.md`, `README.md` | M3 |
| Bảng setup dataset/model/hardware | `data/preprocess.py`, `models/`, `train.py` | M4 |
| Kết quả E1/E2/E3 hoặc preliminary result | `train.py`, `evaluate.py` | M5 |
| Plot/bảng kết quả | `results/plots/reproduce_runtime.png` hoặc plot mới | M5-M6 |
| Speaker notes + Q&A reproduction | `docs/phan_cong_present_hyena_3_tuan.md` | M6-M7 |

---

## 5. Agenda Call Sync-Up Chung

Thời lượng đề xuất: **60-75 phút**.

| Phần | Thời lượng | Nội dung |
|---|---:|---|
| 1. Check mục tiêu chung | 5 phút | Nhắc lại mạch: problem -> Hyena -> paper results -> reproduction |
| 2. TV1 trình bày thử | 12-15 phút | Slide 1-11, cả nhóm ghi chỗ chưa rõ |
| 3. Feedback TV1 | 5 phút | Có quá dài không, có nối được sang TV2 không |
| 4. TV2 trình bày thử | 12-15 phút | Slide 12-22, tập trung recurrence/FFTConv/paper results |
| 5. Feedback TV2 | 5 phút | Slide nào khó, có cần tách/bớt công thức không |
| 6. TV3 trình bày thử | 12-15 phút | Slide 23-33, đặc biệt kết quả E1/E2/E3 |
| 7. Feedback TV3 | 5 phút | Số liệu đã rõ chưa, có tách paper vs nhóm chưa |
| 8. Q&A thử | 10 phút | Mỗi người hỏi người khác 2 câu |
| 9. Chốt việc sau call | 5 phút | Ai sửa gì, deadline sửa |

---

## 6. Checklist Trước Call Sync-Up

### Cả nhóm

- [ ] Mỗi người có bullet slide phần mình.
- [ ] Mỗi người có ít nhất 5 câu Q&A phần mình.
- [ ] Có câu chuyển tiếp TV1 -> TV2 và TV2 -> TV3.
- [ ] Không lẫn kết quả paper gốc với kết quả nhóm.

### TV1

- [ ] Giải thích được vì sao Attention là `O(L^2)`.
- [ ] Có bảng related work ngắn.
- [ ] Có câu chuyển sang Hyena: cần operator rẻ hơn nhưng vẫn data-controlled.

### TV2

- [ ] Giải thích được long convolution, gating, recurrence, implicit filter, FFTConv.
- [ ] Có bảng complexity.
- [ ] Có bảng kết quả paper gốc.
- [ ] Ghi rõ kết quả slide 22 là của paper.

### TV3

- [ ] Có bảng dataset/model/hardware.
- [ ] Có E1/E2/E3 hoặc ghi rõ preliminary.
- [ ] Có plot hoặc bảng số liệu cho slide 30-31.
- [ ] Có phần giới hạn reproduction trung thực.

---

## 7. Các Điểm Nghẽn Cần Theo Dõi

| Điểm nghẽn | Tác động | Cách xử lý |
|---|---|---|
| Chưa có số liệu E1/E2/E3 | Slide 30-31 yếu | Chạy tối thiểu E2/E3 trước, E1 có thể preliminary |
| TV2 quá toán ở FFT/matrix view | Người nghe khó theo | Nói trực giác, không chứng minh sâu |
| TV1 nói nền quá dài | Lấn thời gian TV2/TV3 | Giữ mỗi slide 60-90 giây |
| TV3 lẫn kết quả paper và nhóm | Dễ bị thầy hỏi | Luôn ghi "paper gốc" vs "kết quả nhóm" |
| Q&A không chia rõ người trả lời | Dễ im lặng/lúng túng | Câu hỏi thuộc phần ai thì người đó trả lời trước |
