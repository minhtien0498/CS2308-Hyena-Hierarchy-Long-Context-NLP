# TV2 - Handoff Notes Với TV1 Và TV3

Mục tiêu: phần TV2 không bị rời rạc, mà nối tự nhiên từ TV1 và chuyển mượt sang TV3.

---

## 1. TV1 Cần Bàn Giao Cho TV2

TV1 nên kết thúc bằng các ý:

- Self-Attention mạnh vì:
  - data-controlled;
  - sublinear parameter scaling;
  - unrestricted context.
- Nhưng attention bị `O(L^2)` vì attention matrix `L x L`.
- Các mô hình subquadratic trước Hyena còn capability gap.

Câu TV1 có thể nói:

> "Như vậy, bài toán là làm sao giữ được các tính chất tốt của Attention nhưng tránh chi phí `O(L^2)`. Phần tiếp theo sẽ trình bày Hyena, một hướng thay thế Attention bằng long convolution và gating."

---

## 2. TV2 Mở Đầu Như Thế Nào

Câu mở đầu TV2:

> "Tiếp nối phần trước, Hyena không cố xấp xỉ trực tiếp attention matrix. Thay vào đó, paper xây một toán tử mới từ hai thành phần rẻ hơn: long convolution để lấy thông tin xa, và gating để điều khiển theo dữ liệu đầu vào."

---

## 3. TV2 Cần Bàn Giao Cho TV3

TV2 nên kết thúc bằng các ý:

- Paper gốc đánh giá Hyena ở quy mô lớn.
- Kết quả paper gốc không phải kết quả nhóm.
- Nhóm chỉ tái hiện quy mô nhỏ để kiểm chứng xu hướng.

Câu TV2 có thể nói:

> "Các kết quả vừa rồi là của paper gốc, với mô hình và tài nguyên lớn hơn nhiều so với phạm vi môn học. Vì vậy, nhóm chọn small-scale reproduction trên WikiText-2 để kiểm chứng xu hướng giữa Transformer-small và Hyena-small."

---

## 4. TV3 Nên Nhận Ý Như Thế Nào

TV3 có thể mở đầu:

> "Dựa trên ý tưởng và kết quả paper gốc, phần của nhóm em không nhằm tái hiện toàn bộ số liệu tuyệt đối, mà tập trung vào trend verification: so sánh PPL/loss và runtime scaling ở quy mô nhỏ."

---

## 5. Các Điểm Không Được Lẫn

| Dễ lẫn | Cách nói đúng |
|---|---|
| Kết quả paper vs kết quả nhóm | "Theo paper gốc..." / "Trong reproduction của nhóm..." |
| Hyena tốt hơn Transformer mọi mặt | "Hyena match Transformer trong một số setting và hiệu quả hơn ở long-context" |
| Hyena luôn nhanh hơn | "Lợi thế rõ hơn khi sequence length lớn; ở L nhỏ có overhead FFT" |
| Hyena là attention approximation | "Hyena là operator mới, không xấp xỉ trực tiếp attention matrix" |

