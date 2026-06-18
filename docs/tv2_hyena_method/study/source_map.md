# TV2 - Source Map

File này chỉ ra từng slide nên lấy thông tin từ đâu để tránh đọc lan man.

---

## Nguồn Chính

| Nguồn | Dùng cho |
|---|---|
| `docs/paper_summary.md` | Contribution, method, paper results |
| `docs/comparison_table.md` | Complexity, data control, Transformer vs Hyena |
| `docs/related_work_notes.md` | H3, GSS, SSM, Mamba |
| `models/hyena.py` | Liên hệ code: `HyenaFilter`, `HyenaOperator`, FFTConv |
| `slides/slide_outline.md` | Mạch slide chung 33 slide |
| `docs/poli23a.pdf` | Nguồn gốc nếu cần đối chiếu figure/table |

---

## Map Theo Slide

| Slide | Chủ đề | Nguồn nên đọc |
|---:|---|---|
| 12 | Từ Attention sang Hyena | `docs/paper_summary.md` Section 2-3 |
| 13 | Ý tưởng chính | `docs/paper_summary.md` Section 4 |
| 14 | Long convolution | `docs/comparison_table.md`, `docs/paper_summary.md` Section 4 |
| 15 | Gating/data-controlled | `docs/comparison_table.md` phần Data Control |
| 16 | Hyena recurrence | `docs/paper_summary.md` Section 4.1, `models/hyena.py` docstring |
| 17 | Order-N hierarchy | `docs/related_work_notes.md` phần Hyena/H3 |
| 18 | Matrix view | `docs/paper_summary.md` contribution #3, `slides/slides.md` nếu cần tham khảo |
| 19 | Implicit filter | `docs/paper_summary.md` Section 4.2, `models/hyena.py -> HyenaFilter` |
| 20 | FFTConv | `docs/comparison_table.md`, `models/hyena.py -> _causal_fft_conv` |
| 21 | Complexity | `docs/comparison_table.md`, `docs/paper_summary.md` |
| 22 | Paper results | `docs/paper_summary.md` Section 5 |

---

## Code Snippet Nên Biết

Trong `models/hyena.py`:

```python
H = torch.fft.rfft(h, n=fft_len, dim=-1)
V = torch.fft.rfft(v, n=fft_len, dim=-1)
Y = H * V
y = torch.fft.irfft(Y, n=fft_len, dim=-1)[..., :L]
```

Ý nghĩa:

- `rfft`: chuyển sang miền tần số.
- `H * V`: convolution trở thành nhân element-wise.
- `irfft`: quay lại miền thời gian.
- `[..., :L]`: lấy phần causal/đúng độ dài sequence.

---

## Số Liệu Paper Nên Nhớ

| Mục | Số liệu |
|---|---|
| WikiText-103 | Hyena-3 khoảng 18.6 PPL, gần Transformer 18.6 |
| The Pile 335M | Hyena-2 khoảng 9.2 PPL, Transformer khoảng 9.1 |
| FLOPs | Hyena giảm khoảng 20% non-parametric FLOPs |
| Runtime 8K | Khoảng 2x so với FlashAttention |
| Runtime 64K | Khoảng 100x so với FlashAttention |

Khi nói số liệu, nên dùng từ "theo paper gốc" để tránh nhầm với reproduction của nhóm.

