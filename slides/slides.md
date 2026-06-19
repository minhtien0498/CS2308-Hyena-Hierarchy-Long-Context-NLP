---
marp: true
title: "Hyena Hierarchy — TV2 + TV3"
author: "Tô Huỳnh Minh Tiến · Kiên (Nhóm 08)"
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
  code { background:#e7edf6; color:#1F3A68; padding:1px 6px; border-radius:4px; }
  ul { list-style:none; padding-left:6px; }
  ul li { position:relative; padding-left:24px; margin:10px 0; }
  ul li::before { content:"●"; color:#1F3A68; font-size:14px; position:absolute; left:0; top:4px; }
  ol li { margin:10px 0; }
  table { font-size:21px; border-collapse:collapse; margin:6px 0; }
  th { background:#1F3A68; color:#ffffff; }
  td { background:#ffffff; }
  td,th { border:1px solid #c3d2ea; padding:5px 12px; }
  blockquote { border-left:4px solid #1F3A68; background:#e7edf6; color:#20324f; padding:8px 18px; }
  footer { left:0; bottom:0; width:100%; box-sizing:border-box;
           display:flex; padding:0; height:26px; font-size:13px; color:#ffffff;
           background:linear-gradient(90deg,#0e1d38 0%,#16294d 30%,#1f3a68 62%,#2a4d86 100%); }
  footer span { flex:1; display:flex; align-items:center; justify-content:center;
                border-right:1px solid rgba(255,255,255,.3); }
  footer span:nth-child(4) { flex:0 0 64px; }
  footer span:last-child { border-right:none; }
  section::after { position:absolute; right:18px; bottom:5px; z-index:10;
                   color:#ffffff; font-weight:600; font-size:13px;
                   content: attr(data-marpit-pagination) " / " attr(data-marpit-pagination-total); }
  header { position:absolute; top:9px; right:16px; left:auto; margin:0; padding:0;
           background:none; box-shadow:none; z-index:40; }
  header img { height:50px; width:50px; object-fit:contain; display:block; background:#ffffff;
               border-radius:50%; padding:5px; box-sizing:border-box;
               box-shadow:0 1px 5px rgba(0,0,0,.22); }
  section.lead { text-align:center; justify-content:flex-start; }
  .titlebox { width:100%; box-sizing:border-box; background:#1F3A68;
    border-radius:10px; padding:24px 40px; margin:48px 0 30px 0;
    box-shadow:0 5px 12px rgba(0,0,0,.18); text-align:center; }
  .titlebox h1 { background:none; border:none; box-shadow:none; display:block;
    color:#ffffff !important; font-size:38px; margin:0; padding:0; }
  .titlebox h3 { color:#ffffff !important; font-weight:400; margin:8px 0 0 0; }
  section.lead h1 { color:#1F3A68; font-size:42px; }
  section.lead h3 { color:#1d2b36; font-weight:400; margin-top:0; }
  .thanks h1 { background:none; border:none; box-shadow:none;
    color:#1F3A68 !important; font-size:46px; font-weight:700;
    margin:60px 0 28px 0; padding:0; }
  .small { font-size:18px; color:#777; }
  .box { background:#e7edf6; border:1px solid #c3d2ea; border-radius:10px; padding:12px 20px; }
  .warn { background:#f4f7fb; border:1px solid #c3d2ea; border-radius:10px; padding:12px 20px; }
  .pipeline {
    background:#ffffff;
    border:1px solid #c3d2ea;
    border-radius:10px;
    padding:12px 16px;
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    font-size:20px;
    line-height:1.65;
  }
  .grid2 {
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:18px;
    align-items:start;
  }
  .diagram { text-align:center; margin-top:14px; }
  .diagram img { max-height:300px; width:auto; }
footer: '<span>Nhóm 08 · CS2308</span><span>TV2 + TV3 · Hyena Hierarchy</span><span>2026</span><span></span>'
header: '<img src="assets/UIT_logo.svg" alt="UIT">'
---

<!-- _class: lead -->
<!-- _paginate: false -->

<div class="titlebox">

# Hyena Hierarchy
### TV2 Method + TV3 Reproduction

</div>

<span class="small">Bài báo: Poli, Massaroli, Nguyen, Dao, Baccus, Bengio, Ermon, Re · ICML 2023</span>

<br>

**Nhóm 08 · CS2308**
Tô Huỳnh Minh Tiến · Kiên

<span class="small">Deck ghép phần TV2 và TV3 để ráp present chung</span>

---

## Nội dung trình bày

1. **TV2 - Hyena method**: từ attention sang long convolution + gating
2. **TV2 - Paper results**: quality và efficiency của paper gốc
3. **TV3 - Reproduction**: setup nhóm trên WikiText-2
4. **TV3 - Kết quả**: perplexity, runtime scaling, giới hạn

---

<!-- _class: lead -->

# TV2
### Hyena Method & Paper Results

---

## Từ Attention Sang Hyena

<div class="box">

**Câu hỏi TV2 cần trả lời:** Hyena thay thế self-attention bằng toán tử nào, và vì sao toán tử đó rẻ hơn khi context dài?

</div>

| Attention làm tốt | Vấn đề khi `L` dài | Hyena thay bằng |
|---|---|---|
| Trộn thông tin toàn chuỗi | Ma trận `L × L` | **Long convolution** |
| Chọn lọc theo nội dung input | `O(L²)` time/memory | **Data-controlled gating** |
| Chất lượng LM mạnh | Khó mở rộng long-context | **FFTConv `O(L log L)`** |

```text
TV1: Attention bottleneck  ->  TV2: Hyena operator  ->  TV3: small reproduction
```

---

## Ý Tưởng Chính Của Hyena

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

---

## Long Convolution

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

---

## Data-Controlled Gating

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

---

## Hyena Recurrence

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

---

## Order-N Hierarchy

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

---

## Matrix View

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

---

## Implicit Filter

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

---

## FFTConv

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

---

## Complexity Và Ý Nghĩa

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

---

## Kết Quả Paper Gốc

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
    <tr><td>64K</td><td>>100x trong paper</td></tr>
  </tbody>
</table>
</div>

</div>

<div class="box">

Đây là kết quả của **paper gốc**, không phải kết quả reproduction của nhóm.

</div>

---

<!-- _class: lead -->

# TV3
### Small-Scale Reproduction Trên WikiText-2

---

## Phạm vi & mục tiêu

Nhóm không tái hiện toàn bộ paper, vì The Pile 800GB và GPU lớn vượt quá tài nguyên môn học. Thay vào đó nhóm làm tái hiện ở quy mô nhỏ, mục tiêu là kiểm chứng xu hướng chứ không khớp số tuyệt đối.

<div class="box">

Hai câu hỏi nhóm muốn tự trả lời:
1. Ở quy mô nhỏ, perplexity của Hyena có ngang Transformer không?
2. Khi chuỗi dài ra, Hyena có lợi thế tốc độ như paper dự đoán không?

</div>

Code do nhóm tự cài bằng thuần PyTorch, có đối chiếu với bản chính chủ `HazyResearch/safari`.

---

## Thiết lập thực nghiệm

Dữ liệu: WikiText-2, tokenizer GPT-2, cắt chuỗi theo độ dài 256.

| Cấu hình | Transformer-small | Hyena-small |
|---|---|---|
| Layers | 4 | 4 |
| `d_model` / `d_ff` | 256 / 1024 | 256 / 1024 |
| Trộn thông tin | 4 heads attention | order N=2, FFTConv |
| Params | 16.1M | 16.3M |

Hyena dùng `torch.fft.rfft` thuần PyTorch, không có custom CUDA kernel.  
Huấn luyện bằng AdamW kèm warmup rồi cosine, đánh giá bằng val loss quy ra perplexity, chạy trên Colab T4.

---

## Kết quả E1: Perplexity (L=256)

| Model | Val loss | Val PPL |
|---|---|---|
| Transformer-small | 5.69 | 295.6 |
| Hyena-small | 5.53 | 251.8 |

<span class="small">Kết quả sơ bộ sau 5 epoch, chạy bằng `notebooks/colab_E1_run.ipynb`. Loss vẫn đang giảm nên đây là số minh hoạ xu hướng, chưa phải mức hội tụ cuối.</span>

Nhận xét: hai model cùng cỡ tham số cho perplexity cùng tầm, Hyena còn nhỉnh hơn một chút. Đủ để nói Hyena là một baseline ngôn ngữ hợp lệ ở quy mô này.

---

## Kết quả: tốc độ theo độ dài chuỗi

Đo thời gian forward với input giả, cùng cấu hình model 16M tham số, batch 8, trên Colab T4.

| L | Transformer (ms) | Hyena (ms) | Tỉ lệ |
|---|---|---|---|
| 256 | 21.4 | 21.9 | Hyena chậm hơn chút |
| 512 | 43.7 | 42.4 | hai bên hòa nhau |
| 1024 | 100.1 | 84.1 | Hyena nhanh hơn ~1.19 lần |

Ở L=2048 Hyena vẫn chạy tốt khoảng 168 ms, trong khi Transformer bắt đầu đuối. Attention tăng theo bình phương độ dài, còn Hyena tăng gần tuyến tính, nên chuỗi càng dài Hyena càng lợi.

---

## Thảo luận và giới hạn

- Ở chuỗi ngắn Hyena chậm hơn, vì chi phí FFT và đệm 2L lớn hơn phần tiết kiệm được.
- Hyena hòa ở khoảng L = 512 và vượt lên từ L = 1024, đúng như lưu ý trong paper.
- Bản cài của nhóm đơn giản hóa so với safari: filter dùng SiLU thay cho activation dạng sin, modulation rút gọn, bỏ skip-connection.
- Vì dùng thuần PyTorch và không có CUDA kernel, nhóm chưa đạt mức speedup tuyệt đối như paper.
- Phần đo tốc độ dùng input giả để đo thời gian forward, không phải đánh giá perplexity trên tập validation.

---

## Kết luận phần tái hiện

- Nhóm tự cài Hyena bằng thuần PyTorch, phần lõi khớp với bản chính chủ ở FFTConv đệm 2L, short conv depthwise và gating đệ quy bậc N.
- Quan sát đúng xu hướng chính của bài: tốc độ Hyena tăng gần tuyến tính, attention tăng theo bình phương, hai đường giao nhau quanh L = 512 và Hyena vượt lên rõ từ L = 1024.
- Bài học rút ra: hiểu được vì sao attention nghẽn ở chuỗi dài, và thấy được giới hạn thực tế của tái hiện khi thiếu kernel tối ưu và tài nguyên.

> Quy mô nhỏ nhưng đủ để thấy tận mắt cơ chế dưới bậc hai mà bài báo đề xuất.

---

<!-- _class: lead -->

<div class="thanks">

# Cảm ơn! · Q&A

</div>

**Nhóm 08 · CS2308**
Tô Huỳnh Minh Tiến · Kiên

<span class="small">Tài liệu: Poli et al., *Hyena Hierarchy*, ICML 2023 · `docs/poli23a.pdf`</span>
