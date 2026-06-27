---
marp: true
title: "Hyena Hierarchy — Towards Larger Convolutional Language Models"
author: "Trần Tú Quang · Tô Huỳnh Minh Tiến · Kiên (Nhóm 08)"
paginate: true
html: true
math: katex
backgroundColor: "#ffffff"
color: "#1d2b36"
style: |
  @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,400;0,600;0,700;1,400&display=swap');
  section {
    font-family: "Be Vietnam Pro", "Segoe UI", system-ui, sans-serif;
    font-size: 24px;
    padding: 100px 64px 64px 64px;
    background: #ffffff;
    color: #1d2b36;
    display: flex;
    flex-direction: column;
    justify-content: flex-start !important;
    align-content: flex-start;
  }
  h2 {
    position: absolute;
    top: 0; left: 0; right: 0;
    margin: 0;
    background: #1F3A68;
    color: #ffffff !important;
    font-size: 30px;
    font-weight: 600;
    padding: 16px 64px;
  }
  h3 { color:#1F3A68; font-size:24px; margin-bottom:4px; }
  strong { color:#1F3A68; }
  em { color:#1d4ed8; font-style:normal; }
  a { color:#1F3A68; }
  code {
    background: #e7edf6;
    color: #1F3A68;
    padding: 1px 6px;
    border-radius: 4px;
  }
  ul { list-style:none; padding-left:6px; }
  ul li { position:relative; padding-left:24px; margin:10px 0; }
  ul li::before { content:"●"; color:#1F3A68; font-size:14px; position:absolute; left:0; top:4px; }
  ol li { margin:10px 0; }
  table {
    font-size: 21px;
    border-collapse: collapse;
    margin: 6px 0;
  }
  th { background:#1F3A68; color:#ffffff; }
  td { background:#ffffff; }
  td, th { border:1px solid #c3d2ea; padding:5px 12px; }
  blockquote {
    border-left:4px solid #1F3A68;
    background:#e7edf6;
    color:#20324f;
    padding:8px 18px;
  }
  footer {
    left:0;
    bottom:0;
    width:100%;
    box-sizing:border-box;
    display:flex;
    padding:0;
    height:26px;
    font-size:13px;
    color:#ffffff;
    background:linear-gradient(90deg,#0e1d38 0%,#16294d 30%,#1f3a68 62%,#2a4d86 100%);
  }
  footer span {
    flex:1;
    display:flex;
    align-items:center;
    justify-content:center;
    border-right:1px solid rgba(255,255,255,.3);
  }
  footer span:nth-child(4) { flex:0 0 64px; }
  footer span:last-child { border-right:none; }
  section::after {
    position:absolute;
    right:18px;
    bottom:5px;
    z-index:10;
    color:#ffffff;
    font-weight:600;
    font-size:13px;
    content: attr(data-marpit-pagination) " / " attr(data-marpit-pagination-total);
  }
  header {
    position:absolute;
    top:9px;
    right:16px;
    left:auto;
    margin:0;
    padding:0;
    background:none;
    box-shadow:none;
    z-index:40;
  }
  header img {
    height:50px;
    width:50px;
    object-fit:contain;
    display:block;
    background:#ffffff;
    border-radius:50%;
    padding:5px;
    box-sizing:border-box;
    box-shadow:0 1px 5px rgba(0,0,0,.22);
  }
  section.lead {
    text-align: center;
    justify-content: flex-start;
  }
  .titlebox {
    width:100%;
    box-sizing:border-box;
    background:#1F3A68;
    border-radius:10px;
    padding:24px 40px;
    margin:48px 0 30px 0;
    box-shadow:0 5px 12px rgba(0,0,0,.18);
    text-align:center;
  }
  .titlebox h1 {
    background:none;
    border:none;
    box-shadow:none;
    display:block;
    color:#ffffff !important;
    font-size:38px;
    margin:0;
    padding:0;
  }
  .titlebox h3 { color:#ffffff !important; font-weight:400; margin:8px 0 0 0; }
  section.lead h1 { color:#1F3A68; font-size:42px; }
  section.lead h3 { color:#1d2b36; font-weight:400; margin-top:0; }
  .small {
    font-size:18px;
    color:#777;
  }
  .box {
    background:#e7edf6;
    border:1px solid #c3d2ea;
    border-radius:10px;
    padding:12px 20px;
  }
  .warn {
    background:#f4f7fb;
    border:1px solid #c3d2ea;
    border-radius:10px;
    padding:12px 20px;
  }
  .pipeline {
    background:#ffffff;
    border:1px solid #c3d2ea;
    border-radius:10px;
    padding:12px 16px;
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    font-size: 20px;
    line-height: 1.65;
  }
  .pill {
    display: inline-block;
    border: 1px solid #d1d5db;
    background: #ffffff;
    color: #111827;
    border-radius: 999px;
    padding: 3px 10px;
    margin: 3px 4px 3px 0;
    font-size: 18px;
  }
  .grid2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
    align-items: start;
  }
  .center {
    text-align: center;
  }
  .tight table {
    font-size: 18px;
  }
  .tight li {
    font-size: 22px;
  }
footer: '<span>Nhóm 08 · CS2308</span><span>Hyena Hierarchy (ICML 2023)</span><span>2026</span><span></span>'
header: '<img src="./assets/UIT_logo.svg" alt="UIT">'
---

<!-- _class: lead -->
<!-- _paginate: false -->

<div class="titlebox">

# Hyena Hierarchy
### Towards Larger Convolutional Language Models

</div>

<span class="small">Bài báo: Poli, Massaroli, Nguyen, Dao, Baccus, Bengio, Ermon, Ré · Stanford & Mila · ICML 2023 (PMLR 202)</span>

<br>

**Nhóm 08 · CS2308**
Trần Tú Quang · Tô Huỳnh Minh Tiến · Kiên

<span class="small">Phần phụ trách: Tô Huỳnh Minh Tiến · Hyena method và paper results</span>

<!--
Notes:
Mở đầu phần TV2 sau khi TV1 đã nói về Attention O(L^2).
Mục tiêu: giải thích Hyena hoạt động như thế nào và paper gốc chứng minh gì.
-->

---

## Nội dung trình bày

1. **Từ attention sang Hyena**: bài toán và ý tưởng thay thế self-attention
2. **Cơ chế Hyena**: long convolution, gating, recurrence, hierarchy
3. **Hiện thực hiệu quả**: matrix view, implicit filter, FFTConv
4. **Complexity và paper results**: vì sao Hyena lợi ở long-context

---

## 1. Từ Attention Sang Hyena

<div class="box">

**Câu hỏi trọng tâm:** Hyena thay thế self-attention bằng toán tử nào, và vì sao toán tử đó rẻ hơn khi context dài?

</div>

| Attention làm tốt | Vấn đề khi `L` dài | Hyena thay bằng |
|---|---|---|
| Trộn thông tin toàn chuỗi | Ma trận `L × L` | **Long convolution** |
| Chọn lọc theo nội dung input | `O(L²)` time/memory | **Data-controlled gating** |
| Chất lượng LM mạnh | Khó mở rộng long-context | **FFTConv `O(L log L)`** |

<span class="small">Điểm quan trọng: Hyena không tối ưu attention cũ, mà đề xuất một operator attention-free mới.</span>

<!--
Notes:
Phân công nói: Kiên -> attention bottleneck; Tiến -> Hyena operator; Quang -> small-scale reproduction.
Nhấn mạnh Hyena không phải "attention approximation".
Đây là slide chuyển ý từ phần TV1 sang phần method: vấn đề không chỉ là tốc độ, mà là tìm operator thay thế vẫn đủ expressive cho language modeling.
-->

---

## 2. Ý Tưởng Chính Của Hyena

### Hyena = Long Convolution + Data-Controlled Gating

<div class="grid2">

<div>
<strong>Long convolution</strong>
<ul>
  <li>Filter dài gần bằng sequence.</li>
  <li>Mang tín hiệu từ token xa.</li>
  <li>Tính nhanh bằng FFTConv.</li>
</ul>

</div>

<div>
<strong>Gating</strong>
<ul>
  <li>Sinh từ projection của input.</li>
  <li>Nhân element-wise với output conv.</li>
  <li>Tạo tính content-aware.</li>
</ul>

</div>

</div>

<div class="pipeline">
Input u<br>
 -> linear projections: x1, x2, ..., v<br>
 -> z1 = v<br>
 -> repeat: z(n+1) = gate xn * Conv(hn, zn)<br>
 -> output y
</div>

<span class="small">Câu nói ngắn: convolution truyền thông tin xa, gating quyết định giữ thông tin nào.</span>

<!--
Notes:
Đây là slide bản đồ. Các slide 14-20 sẽ bóc từng mảnh: long conv, gating, recurrence, implicit filter, FFTConv.
-->

---

## 3. Long Convolution

### Từ local kernel sang full-context filter

| Mô hình | Kernel/filter | Phạm vi nhìn |
|---|---|---|
| CNN thường | Ngắn, local | Vài token lân cận |
| Hyena | Dài bằng sequence | Toàn bộ context |

$$
(h * u)_t = \sum_{i=0}^{t} h_{t-i}u_i
$$

```text
CNN local:   token t chỉ nhận từ vùng gần     [x x x] ---- t
Long conv:   token t có thể nhận từ rất xa    [x x x x x x x x x] t
```

**Ý nghĩa:** long convolution giúp mô hình hóa phụ thuộc xa mà không cần ma trận attention `L × L`.

<!--
Notes:
Giải thích công thức ở mức trực giác: output tại t là tổng có trọng số của các token trước đó.
Causal conv chỉ nhìn quá khứ, phù hợp language modeling.
-->

---

## 4. Data-Controlled Gating

### Vì sao cần gating?

- Convolution thuần thường khá **tĩnh**: cùng filter áp dụng cho mọi input.
- Language modeling cần chọn lọc theo **ngữ cảnh input**.
- Hyena dùng gate `xⁿ` được chiếu từ input, rồi nhân với output convolution.

<div class="grid2">

<div class="pipeline">
conv output:<br>
[0.8, 0.4, 0.9, 0.2]<br><br>
gate x:<br>
[1.0, 0.1, 0.7, 0.0]
</div>

<div class="pipeline">
selected signal:<br>
[0.8, 0.04, 0.63, 0.0]<br><br>
gate cao -> giữ<br>
gate thấp -> giảm
</div>

</div>

> Long convolution đưa thông tin từ xa về; gating quyết định thông tin nào nên được giữ lại.

<!--
Notes:
Đây là slide quan trọng để trả lời câu hỏi "Hyena data-controlled như thế nào?"
Gate không phải cổng logic 0/1 cứng; nó là tín hiệu liên tục, học được, phụ thuộc input.
-->

---

## 5. Hyena Recurrence

### Công thức trung tâm

$$
z^{n+1}_t = x^n_t \cdot (h^n * z^n)_t
$$

<div class="grid2">

<div>
<table>
  <thead>
    <tr><th>Thành phần</th><th>Ý nghĩa</th></tr>
  </thead>
  <tbody>
    <tr><td><code>z¹ = v</code></td><td>value stream ban đầu</td></tr>
    <tr><td><code>hⁿ</code></td><td>long filter ở bước <code>n</code></td></tr>
    <tr><td><code>xⁿ_t</code></td><td>gate tại token <code>t</code></td></tr>
    <tr><td><code>N</code></td><td>số bậc/order</td></tr>
  </tbody>
</table>

</div>

<div class="pipeline">
Bước n:<br>
1. lấy z(n)<br>
2. Conv với filter h(n)<br>
3. nhân gate x(n)<br>
4. ra z(n+1)
</div>

</div>

<span class="small">Output cuối: `y = z^(N+1)`.</span>

<!--
Notes:
Đây là slide trọng tâm nhất của TV2. Hãy giải thích từng biến thật chậm.
Nếu bị hỏi "Hyena khác CNN ở đâu?", quay lại đây: CNN chủ yếu conv; Hyena xen kẽ conv dài và gate phụ thuộc input nhiều bước.
-->

---

## 6. Order-N Hierarchy

### Vì sao gọi là "Hierarchy"?

- Hyena có thể lặp nhiều bước **convolution + gating**.
- `N` càng lớn, operator càng biểu diễn phong phú hơn.
- Các cấu trúc như H3/GSS có thể xem là liên quan ở bậc thấp.
- Trong repo nhóm: Hyena-small dùng **`order = 2`** để dễ reproduction.

<div class="pipeline">
Order 1:  z1 -> Conv h1 -> Gate x1 -> z2<br>
Order 2:  z1 -> Conv h1 -> Gate x1 -> z2 -> Conv h2 -> Gate x2 -> z3<br>
Order N:  repeat N lần -> output
</div>

<div class="warn">
Không cần chứng minh hierarchy; chỉ cần nắm: mỗi order thêm một tầng tương tác có cấu trúc.
</div>

<!--
Notes:
Không cần giải thích sâu H3/GSS, chỉ nói Hyena tổng quát hóa ý tưởng gating + convolution.
-->

---

## 7. Matrix View

### Trực giác ma trận

| Thành phần Hyena | Dạng ma trận | Trực giác |
|---|---|---|
| Gating `xⁿ` | Diagonal matrix `Dₓ` | nhân từng vị trí/channel |
| Convolution `hⁿ * zⁿ` | Toeplitz matrix `Sₕ` | trượt cùng một filter qua chuỗi |

<div class="box">

Hyena xen kẽ `Dₓ` và `Sₕ`, thay vì tạo một attention matrix dense `L × L`.

</div>

```text
Attention:    y = A(x) · v        A là dense L x L
Hyena:        y ≈ D_x2 · S_h2 · D_x1 · S_h1 · v
```

<span class="small">Điểm chính: vẫn phụ thuộc input qua `Dₓ`, nhưng tận dụng cấu trúc để tính rẻ hơn.</span>

<!--
Notes:
Đây là slide khó nhất. Chỉ nói trực giác, không chứng minh butterfly decomposition.
Nếu thầy hỏi sâu: D_x là diagonal nên nhân rẻ; S_h có cấu trúc convolution nên tính bằng FFT.
-->

---

## 8. Implicit Filter

### Filter dài nhưng ít tham số

$$
h_t = \mathrm{Window}(t) \cdot \mathrm{FFN}(\mathrm{PE}(t))
$$

| Cách học filter | Ý tưởng | Vấn đề/lợi ích |
|---|---|---|
| Explicit | lưu trực tiếp `h[0...L-1]` | dài hơn thì thêm tham số |
| Implicit | học hàm sinh `h_t` từ vị trí `t` | tham số nằm trong FFN |

<div class="pipeline">
position t -> Positional Encoding -> small FFN -> raw filter value<br>
raw value * Window(t) -> h_t
</div>

<span class="small">Window/decay giúp filter ổn định hơn ở các khoảng cách xa.</span>

<!--
Notes:
Ẩn dụ dễ nói: học một công thức sinh filter thay vì học từng điểm của filter.
Đừng sa vào chi tiết kiến trúc FFN; mục tiêu là hiểu tại sao filter dài không làm số tham số nổ theo L.
-->

---

## 9. FFTConv

### Tính long convolution hiệu quả

<div class="box">

**Ý tưởng:** chuyển convolution sang miền tần số để phép convolution trở thành phép nhân element-wise.

</div>

<div class="pipeline">
1. FFT(h) và FFT(u)<br>
2. Nhân element-wise trong miền tần số<br>
3. iFFT để quay lại sequence output
</div>

| Cách tính | Chi phí trực giác | Khi nào quan trọng |
|---|---|---|
| Direct convolution | tốn hơn khi filter rất dài | ít hợp với long-context |
| FFTConv | khoảng `O(L log L)` | lợi khi `L` lớn |

<span class="small">Trong repo: `models/hyena.py -> HyenaOperator._causal_fft_conv`.</span>


<!--
Notes:
Không cần đi sâu Fourier. Chỉ cần giải thích "đổi miền để convolution thành phép nhân".
Đây là cầu nối giữa công thức paper và code trong repo.
Nếu cần nhắc code:
H = torch.fft.rfft(h, n=fft_len, dim=-1)
V = torch.fft.rfft(v, n=fft_len, dim=-1)
Y = H * V
y = torch.fft.irfft(Y, n=fft_len, dim=-1)[..., :L]
-->

---

<!-- _class: tight -->

## 10. Complexity Và Ý Nghĩa

### Điểm rơi của Hyena là context dài

| Method | Time | Memory |
|---|---|---|
| Standard Attention | `O(L²)` | `O(L²)` |
| FlashAttention | `O(L²)` compute | tối ưu memory access |
| Hyena | `O(N · L log L)` | gần tuyến tính theo `L` |

<div class="box">

Khi `L` tăng rất lớn, `L log L` tăng chậm hơn `L²`, nên lợi thế của Hyena rõ nhất ở long-context.

</div>

<span class="small">Lưu ý khi nói: Hyena không nhất thiết nhanh hơn ở `L` nhỏ vì FFT có overhead.</span>
<span class="small">Giá trị của paper: vừa có novelty kiến trúc, vừa thu hẹp quality gap với Transformer ở long-context.</span>

<!--
Notes:
Nhấn mạnh không nói Hyena luôn nhanh hơn. Lợi thế rõ nhất ở context dài.
FlashAttention vẫn là O(L^2) compute, nhưng tối ưu memory access rất tốt. Vì vậy ở L nhỏ/trung bình có thể vẫn cạnh tranh.
Nếu cần minh họa số:
L = 1K: L^2 khoảng 1M, L log2 L khoảng 10K.
L = 8K: L^2 khoảng 67M, L log2 L khoảng 106K.
L = 64K: L^2 khoảng 4.1B, L log2 L khoảng 1M.
-->

---

## 11. Kết Quả Paper Gốc

### Paper chứng minh 2 thứ: quality và efficiency

<div class="grid2">

<div>
<strong>Quality</strong>
<table>
  <thead>
    <tr><th>Benchmark</th><th>Kết quả</th></tr>
  </thead>
  <tbody>
    <tr><td>WikiText-103</td><td>Hyena-3 ~ Transformer 125M</td></tr>
    <tr><td>The Pile 335M</td><td>Hyena-2 gần Transformer</td></tr>
    <tr><td>Synthetic tasks</td><td>tốt trên recall/reasoning dài</td></tr>
  </tbody>
</table>

</div>

<div>
<strong>Efficiency</strong>
<table>
  <thead>
    <tr><th>Length</th><th>Kết quả runtime</th></tr>
  </thead>
  <tbody>
    <tr><td>2K</td><td>gần crossover</td></tr>
    <tr><td>8K</td><td>~5x vs attention, ~2x vs FlashAttention</td></tr>
    <tr><td>64K</td><td>&gt;100x trong paper</td></tr>
  </tbody>
</table>

</div>

</div>

<div class="box">

Đây là kết quả của **paper gốc**, không phải kết quả reproduction của nhóm.

</div>

<!--
Notes:
Nếu bị hỏi vì sao bài này đáng chú ý: nhấn mạnh novelty không nằm ở việc tối ưu attention cũ, mà ở chỗ paper đề xuất một operator attention-free mới kết hợp long convolution, gating và implicit filter.
Kết thúc bằng câu chuyển sang TV3: paper chạy scale lớn; nhóm sẽ reproduction nhỏ hơn trên WikiText-2 để kiểm tra xu hướng, không claim đạt lại toàn bộ kết quả paper.
-->

---

<!-- _class: lead -->

# Chuyển Sang Reproduction

Các kết quả vừa rồi là của paper gốc ở quy mô lớn.

Trong phạm vi môn học, nhóm thu nhỏ bài toán để kiểm chứng xu hướng trên WikiText-2 với Transformer-small và Hyena-small.

<!--
Notes:
Slide này có thể giữ hoặc bỏ tùy deck chung. Nếu giữ, đây là cầu nối TV2 -> TV3.
-->
