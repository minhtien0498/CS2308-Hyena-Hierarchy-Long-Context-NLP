# Paper Summary — Hyena Hierarchy: Towards Larger Convolutional Language Models
**Phụ trách:** Thành viên 1 (TV1) | **Deadline:** Cuối Tuần 1

> **Hướng dẫn:** Điền vào các mục [ ] sau khi đọc bài báo poli23a.pdf

---

## 1. Thông Tin Bài Báo

| Trường | Thông tin |
|---|---|
| **Tên bài** | Hyena Hierarchy: Towards Larger Convolutional Language Models |
| **Tác giả** | Michael Poli, Stefano Massaroli, Eric Nguyen, et al. |
| **Venue** | ICML 2023 (International Conference on Machine Learning) |
| **Year** | 2023 |
| **Link** | [poli23a.pdf] (file trong thư mục dự án) |
| **Code** | https://github.com/HazyResearch/safari |

---

## 2. Motivation — Vấn Đề Bài Báo Giải Quyết

> *[TV1 điền: 3–5 câu mô tả vấn đề]*

**Vấn đề chính:**
Self-Attention trong Transformer có độ phức tạp O(L²) theo độ dài chuỗi L, gây ra:
- [Điền: hạn chế về memory]
- [Điền: hạn chế về tốc độ]
- [Điền: hạn chế về ứng dụng long-context]

**Câu hỏi nghiên cứu trung tâm:**
> "Liệu có thể thiết kế toán tử subquadratic thay thế attention, đạt chất lượng tương đương Transformer trên large-scale LM, không cần hybridization?"

---

## 3. Contribution — Đóng Góp Chính

> *[TV1 điền sau khi đọc Section 1]*

| # | Đóng góp | Mô tả ngắn |
|---|---|---|
| 1 | Hyena Hierarchy operator | [điền] |
| 2 | Implicit long convolution | [điền] |
| 3 | Matrix decomposition view | [điền] |
| 4 | SotA on WikiText-103 + The Pile | [điền] |
| 5 | Long-context efficiency | [điền] |

---

## 4. Method — Phương Pháp

### 4.1 Hyena Recurrence
> *[TV1 điền: giải thích công thức bằng lời]*

Công thức recurrence:
```
z^(n+1)_t = x^n_t · (h^n * z^n)_t     n = 1,...,N
y_t = z^(N+1)_t
```

Giải thích:
- `z^n`: [điền]
- `x^n`: [điền — vai trò gating]
- `h^n * z^n`: [điền — tích chập dài]
- Complexity: [điền]

### 4.2 Implicit Filter
> *[TV1 điền: giải thích h_t = Window(t) · FFN(PosEnc(t))]*

```
h_t = Window(t) · FFN(PositionalEncoding(t))
```

Tại sao dùng implicit:
- [điền lý do 1]
- [điền lý do 2]

---

## 5. Experiments — Kết Quả Bài Gốc

> *[TV1 điền từ Section 4 của bài báo]*

### WikiText-103
| Model | Perplexity | Params |
|---|---|---|
| Transformer | [điền] | [điền] |
| Hyena | [điền] | [điền] |
| SotA attention-free trước đó | [điền] | [điền] |

### The Pile (335M)
| Model | Perplexity | FLOPs reduction |
|---|---|---|
| Transformer | [điền] | — |
| Hyena | [điền] | [điền]% |

### Long-context Speedup
| Sequence Length | Speedup vs Attention | Speedup vs FlashAttention |
|---|---|---|
| L = 2,048 | [điền] | [điền] |
| L = 8,192 | [điền] | [điền] |
| L = 64,000 | [điền] | [điền] |

---

## 6. Related Work — Vị Trí Của Hyena

> *[TV1 điền: so sánh với các kiến trúc liên quan]*

| Kiến trúc | Năm | Approach | Hyena so sánh thế nào? |
|---|---|---|---|
| Transformer | 2017 | Dense Attention O(L²) | [điền] |
| S4 | 2021 | SSM | [điền] |
| H3 | 2022 | SSM + Gating | [điền — Hyena tổng quát hóa H3] |
| GSS | 2022 | Gated SSM | [điền] |
| Mamba | 2023 | Selective SSM | [điền — ra đời sau Hyena] |

---

## 7. Nhận Xét Cá Nhân

> *[TV1 điền: ít nhất 5 câu nhận xét chủ quan]*

**Điểm mạnh của bài báo:**
1. [điền]
2. [điền]

**Điểm hạn chế / cần cải thiện:**
1. [điền]
2. [điền]

**Điều bất ngờ nhất khi đọc:**
> [điền]

---

*File này là output của Thành viên 1, Tuần 1. Cập nhật lần cuối: ___/2026*
