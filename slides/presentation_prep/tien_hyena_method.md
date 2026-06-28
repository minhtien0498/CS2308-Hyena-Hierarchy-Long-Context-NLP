# Tiến - Gói Chuẩn Bị Phần Hyena Method & Paper Results

Phần này dành cho **Tiến**, tương ứng **slide 12-22** trong plan 45 phút.

## Mục Tiêu Của Tiến

Tiến cần trả lời được câu hỏi:

> Hyena thay thế Self-Attention bằng cơ chế nào, vì sao cơ chế đó có độ phức tạp thấp hơn, và bài báo gốc chứng minh hiệu quả ra sao?

Nói ngắn gọn:

```text
Attention bị O(L^2)
-> Hyena dùng long convolution để nhìn xa
-> Dùng gating để phụ thuộc vào dữ liệu đầu vào
-> Dùng implicit filter để filter dài nhưng ít tham số
-> Dùng FFTConv để tính convolution trong O(L log L)
-> Paper cho thấy Hyena match Transformer ở một số benchmark và nhanh hơn ở long-context
```

## Slide Tiến Phụ Trách

| Slide | Tiêu đề | Mức độ |
|---:|---|---|
| 12 | Từ Attention Sang Hyena | Dễ |
| 13 | Ý Tưởng Chính | Dễ |
| 14 | Long Convolution | Trung bình |
| 15 | Data-Controlled Gating | Trung bình |
| 16 | Hyena Recurrence | Quan trọng |
| 17 | Order-N Hierarchy | Trung bình |
| 18 | Matrix View | Khó nhất trong phần của Tiến |
| 19 | Implicit Filter | Quan trọng |
| 20 | FFTConv | Quan trọng |
| 21 | Complexity và Ý Nghĩa | Quan trọng |
| 22 | Kết Quả Paper Gốc | Dễ-trung bình |

## Cấu Trúc Thư Mục

| Đường dẫn | Mục đích |
|---|---|
| `slides/tien_slide.md` | Bản slide hiện tại của Tiến trong deck chung |
| `study/qna/qna_tv2.md` | Q&A riêng cho phần Hyena method |
| `study/qna/qna_shared_contribution.md` | Block Q&A để copy sang file Q&A chung của nhóm |
| `study/notes/study_notes.md` | Kiến thức cần học và cách hiểu nhanh |
| `study/notes/source_map.md` | Map nguồn tài liệu trong repo/paper cho từng slide |
| `slides/presentation_prep/slide_content.md` | Nội dung từng slide 12-22: bullet, hình/bảng cần có, ý chính |
| `slides/presentation_prep/visual_checklist.md` | Danh sách hình/bảng nên chuẩn bị |
| `slides/presentation_prep/handoff_notes.md` | Câu chuyển và phần cần phối hợp với TV1/TV3 |
| `slides/presentation_prep/speaker_notes.md` | Bản notes cũ/dạng ngắn để tham khảo |
| `planning/milestones.md` | Recap, deadline từng milestone, agenda call sync-up |
| `planning/task_checklist.md` | Checklist toàn bộ việc Tiến cần hoàn thành |

## File Nên Đọc Trong Repo

| File | Đọc phần nào |
|---|---|
| `docs/paper_summary.md` | Section 3-5: contribution, method, experiments |
| `docs/comparison_table.md` | Bảng Transformer vs Hyena, phần FFT và data control |
| `docs/related_work_notes.md` | H3, GSS, Hyena, Mamba |
| `models/hyena.py` | `HyenaFilter`, `HyenaOperator`, `_causal_fft_conv` |
| `slides/slide_outline.md` | Slide 12-22 |

## Phần Nên Nắm Chắc Nhất

1. **Hyena không xấp xỉ attention trực tiếp.**  
   Hyena xây một operator mới có các tính chất giống attention nhưng rẻ hơn.

2. **Long convolution giúp có context dài.**  
   Filter dài bằng toàn sequence nên không bị giới hạn local window như CNN thông thường.

3. **Gating giúp data-controlled.**  
   Nếu chỉ convolution thì filter khá tĩnh; gating từ input giúp output phụ thuộc nội dung chuỗi.

4. **Implicit filter giúp không cần học vector filter dài L.**  
   FFN sinh filter theo vị trí, nên số tham số không tăng tuyến tính với L.

5. **FFTConv giúp giảm chi phí.**  
   Convolution dài tính qua FFT có chi phí `O(L log L)` thay vì tính trực tiếp tốn hơn.

6. **Kết quả paper gốc phải tách khỏi kết quả nhóm.**  
   Tiến chỉ trình bày kết quả của Poli et al.; kết quả nhóm nằm ở phần TV3.

## Câu Chuyển Tiếp

Từ TV1 sang Tiến:

> "Sau khi thấy Attention có ba tính chất mạnh nhưng bị giới hạn bởi chi phí `O(L^2)`, phần tiếp theo sẽ trình bày Hyena: một toán tử không dùng attention nhưng cố gắng giữ lại các tính chất quan trọng đó bằng long convolution và gating."

Từ Tiến sang TV3:

> "Các kết quả vừa trình bày là của paper gốc ở quy mô lớn. Trong phạm vi môn học, nhóm thu nhỏ bài toán để kiểm chứng xu hướng trên WikiText-2 với Transformer-small và Hyena-small."

## Gợi Ý Tìm File Nhanh

- Muốn sửa phần slide hiện tại của Tiến: vào `slides/tien_slide.md`
- Muốn luyện nói và ôn câu hỏi: vào `study/qna/`
- Muốn xem tài liệu chuẩn bị cũ hơn: vào `slides/presentation_prep/`
