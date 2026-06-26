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
header: '<img src="../../slides/assets/UIT_logo.svg" alt="UIT">'
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
Ở phần này, em mở đầu sau khi TV1 đã trình bày điểm nghẽn chính của self-attention là chi phí `O(L^2)` khi sequence length tăng lên. Mục tiêu của phần TV2 là trả lời hai câu hỏi: nếu không dùng self-attention thì Hyena dùng toán tử nào để thay thế, và vì sao toán tử đó vẫn có thể mô hình hóa phụ thuộc xa nhưng scale tốt hơn khi context dài.

Có thể mở bằng câu: "Ở phần trước, nhóm đã thấy attention rất mạnh nhưng bị nghẽn khi sequence dài. Phần này em sẽ trình bày Hyena như một hướng attention-free để giữ context dài nhưng scale rẻ hơn."

Nếu muốn đặt kỳ vọng cho người nghe ngay từ đầu, có thể nói thêm: "Phần này em không đi qua toàn bộ chi tiết toán học của paper, mà tập trung vào trực giác, cơ chế vận hành, và ý nghĩa về complexity."
-->

---

## Nội dung trình bày

1. **Từ attention sang Hyena**: bài toán và ý tưởng thay thế self-attention
2. **Cơ chế Hyena**: long convolution, gating, recurrence, hierarchy
3. **Hiện thực hiệu quả**: matrix view, implicit filter, FFTConv
4. **Complexity và paper results**: vì sao Hyena lợi ở long-context

<!--
Notes:
Slide này dùng để báo trước mạch nói của cả phần TV2. Em có thể nói ngắn gọn: "Phần này sẽ đi theo đúng trình tự: đầu tiên là từ bài toán attention sang ý tưởng Hyena, sau đó là cơ chế bên trong của Hyena, tiếp theo là cách hiện thực hiệu quả, và cuối cùng là complexity cùng kết quả của paper gốc."

Nếu muốn mượt hơn, có thể thêm: "Nói đơn giản, em sẽ đi từ câu hỏi Hyena là gì, hoạt động ra sao, tính nhanh bằng cách nào, và paper chứng minh được điều gì."
-->

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
Đây là slide chuyển ý quan trọng nhất giữa TV1 và TV2. Ở đây, em nên nhấn mạnh rằng Hyena không phải là một bản xấp xỉ attention theo kiểu làm attention nhanh hơn, mà là một operator khác hẳn, được thiết kế để giữ khả năng truyền thông tin xa và tính linh hoạt theo input.

Em có thể nói: "Nếu nhìn vào bảng này, attention có ba điểm mạnh. Thứ nhất, nó trộn thông tin trên toàn bộ chuỗi. Thứ hai, nó có tính chọn lọc theo nội dung input. Thứ ba, nó cho chất lượng language modeling rất tốt. Vấn đề là khi `L` dài, attention phải xử lý một ma trận `L x L`, nên time và memory đều tăng rất nhanh. Ý tưởng của Hyena là tách bài toán này thành ba mảnh thay thế: dùng long convolution để truyền thông tin xa, dùng data-controlled gating để giữ tính content-aware, và tính convolution bằng FFTConv để có chi phí gần `O(L log L)`."

Sau đó chốt một câu để tránh hiểu nhầm: "Vì vậy, cách nghĩ đúng ở đây không phải là Hyena có một attention matrix ẩn bên trong, mà là Hyena thay cả cơ chế đó bằng một operator có cấu trúc khác."

Nếu muốn tạo ấn tượng ngay ở đầu phần method, có thể nói thêm: "Điểm đáng chú ý của paper không chỉ là giảm độ phức tạp, mà là họ dám thay attention bằng một toán tử mới mà vẫn giữ được mục tiêu language modeling."
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
Đây là slide bản đồ của cả phần method. Em không cần nói quá sâu từng ô trên slide, mà dùng nó để cho người nghe biết phần sau sẽ giải quyết từng ý như thế nào.

Một cách nói tự nhiên là: "Nếu tóm gọn Hyena trong một câu, thì Hyena bằng long convolution cộng với data-controlled gating. Đầu vào sẽ được chiếu thành nhiều stream, trong đó có stream giá trị và các stream gate. Sau đó mô hình lặp đi lặp lại một thao tác: lấy signal hiện tại, cho nó đi qua một long convolution, rồi dùng gate phụ thuộc input để giữ hoặc giảm từng phần thông tin. Cuối cùng, sau nhiều bước như vậy, ta thu được output."

Để mở đường cho các slide sau, có thể nói thêm: "Từ đây em sẽ tách Hyena thành 5 câu hỏi nhỏ: long convolution là gì, gating để làm gì, recurrence hoạt động ra sao, vì sao filter dài không làm nổ tham số, và vì sao tính nhanh được bằng FFT."

Nếu muốn nói thật đời thường, có thể chốt: "Convolution phụ trách mang thông tin xa về, còn gating phụ trách quyết định giữ thông tin nào."
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
Đây là slide để tạo trực giác rằng Hyena vẫn có thể nhìn xa mà không cần attention matrix dày đặc. Điểm cần nhấn mạnh là sự khác nhau giữa convolution ngắn trong CNN thường và long convolution trong Hyena.

Em có thể nói: "Trong CNN thông thường, kernel rất ngắn, ví dụ chỉ nhìn vài token lân cận. Như vậy mô hình xử lý tốt local pattern nhưng khó nhớ được quan hệ rất xa nếu không xếp rất nhiều tầng. Còn trong Hyena, filter có độ dài gần bằng sequence, nên một token ở vị trí `t` có thể nhận ảnh hưởng từ rất nhiều token trước đó, thực chất là từ toàn bộ phần lịch sử cần thiết."

Khi chỉ vào công thức, không cần đọc ký hiệu quá máy móc. Có thể nói: "Công thức này nói rằng output tại thời điểm `t` là tổng có trọng số của các token trước đó. Mỗi token trong quá khứ đóng góp một lượng nào đó, và mức đóng góp đó được điều khiển bởi filter `h`."

Sau đó chốt ý nghĩa: "Vì đây là causal convolution nên nó chỉ nhìn về quá khứ, phù hợp với language modeling. Như vậy, Hyena vẫn có cách để kết nối thông tin xa nhưng không cần xây một ma trận attention `L x L` cho mọi cặp token."

Nếu muốn ví dụ đời thường: "Self-attention giống như mỗi token đi hỏi từng token khác xem có liên quan không. Còn long convolution thì giống như dùng một mẫu có cấu trúc để quét qua lịch sử và tổng hợp lại."
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
Sau khi nói về convolution, slide này trả lời câu hỏi quan trọng nhất: nếu chỉ dùng convolution thì có bị quá tĩnh và thiếu linh hoạt không. Câu trả lời của Hyena là có gating phụ thuộc input.

Em có thể nói: "Nếu chỉ dùng convolution thuần túy, thì vấn đề là cùng một filter sẽ áp dụng cho mọi input, trong khi language modeling cần khả năng chọn lọc theo ngữ cảnh. Cùng là một token, nhưng trong câu này nó có thể quan trọng, sang câu khác thì không. Vì vậy Hyena thêm một cơ chế gating."

Khi chỉ vào ví dụ số trên slide, có thể nói: "Ở đây, conv output có thể xem là thông tin đã được mang về từ xa. Nhưng gate mới quyết định phần nào được giữ mạnh, phần nào bị giảm. Gate lớn thì thông tin được truyền qua nhiều hơn, gate nhỏ thì bị làm yếu đi."

Sau đó chốt rõ: "Đây là lý do paper dùng cụm từ data-controlled. Filter có cấu trúc để tính hiệu quả, nhưng khả năng chọn lọc lại vẫn do dữ liệu đầu vào điều khiển."

Nếu bị hỏi gate có phải 0/1 không thì trả lời: "Không. Gate là một tín hiệu liên tục học được, nên nó mềm và linh hoạt hơn rất nhiều so với một công tắc bật tắt đơn giản."
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
Đây là slide trọng tâm nhất của phần TV2, vì nó viết ra công thức cốt lõi của operator. Ở slide này, tốc độ nói nên chậm hơn một chút và giải thích lần lượt từng biến.

Em có thể nói: "Công thức trung tâm của Hyena là `z^{n+1}_t = x^n_t · (h^n * z^n)_t`. Mình đọc nó theo trực giác như sau. Đầu tiên, `z^n` là signal hiện tại ở bước `n`. Signal này được đưa qua một long convolution với filter `h^n`, nghĩa là ta tổng hợp thông tin từ lịch sử. Sau đó, kết quả tại vị trí `t` được nhân với gate `x^n_t`, là gate sinh ra từ input. Kết quả sau cùng trở thành `z^{n+1}` để đưa sang bước tiếp theo."

Khi chỉ vào bảng, nói rõ từng thành phần: "`z^1 = v` là value stream ban đầu; `h^n` là filter ở bước thứ `n`; `x^n_t` là gate tại token `t`; còn `N` là số lần lặp, hay còn gọi là order của Hyena."

Sau đó chốt mạch vận hành: "Như vậy, mỗi bước của Hyena đều có hai thao tác nối tiếp nhau: convolution để trộn thông tin có cấu trúc, rồi gating để chọn lọc theo input. Lặp lại nhiều bước như vậy sẽ tạo ra một operator mạnh hơn một convolution đơn lẻ."

Nếu bị hỏi Hyena khác CNN ở đâu, quay lại đúng slide này và trả lời: "CNN thường là xếp các lớp convolution. Còn Hyena xen kẽ long convolution và gate phụ thuộc input ở nhiều bước, nên mức độ data-control rõ hơn."
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
Slide này giải thích vì sao tên paper có chữ "Hierarchy". Em không cần đi qua các liên hệ lịch sử như H3 hay GSS quá kỹ, chỉ cần giữ một trực giác rõ ràng về việc lặp nhiều tầng tương tác.

Một cách nói đơn giản là: "Hyena không nhất thiết chỉ có một bước convolution rồi xong. Nó có thể lặp nhiều bước convolution cộng gating. Mỗi lần lặp như vậy thêm một tầng xử lý có cấu trúc, nên paper gọi đây là hierarchy. Khi `N` tăng, operator có khả năng biểu diễn phong phú hơn."

Sau đó liên hệ với repo nhóm: "Trong reproduction của nhóm, để bài toán gọn và dễ chạy ổn định hơn, mình dùng cấu hình nhỏ với `order = 2`, tức là lặp hai lần theo mạch conv rồi gate."

Nếu bị hỏi về H3/GSS, chỉ cần nói ngắn gọn: "Paper xem Hyena như một họ toán tử tổng quát hơn; một số cấu trúc cũ như H3 hoặc GSS có thể xem là trường hợp bậc thấp hoặc liên quan."
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
Đây là slide khó nhất, nên em chỉ cần nói trực giác chứ không chứng minh chi tiết. Mục tiêu là giúp người nghe thấy vì sao Hyena vẫn phụ thuộc input nhưng không cần một attention matrix dense.

Em có thể nói: "Nếu viết dưới dạng ma trận, gating `x^n` có thể xem là một diagonal matrix `D_x`, vì nó chỉ nhân theo từng vị trí. Còn convolution có thể xem là một Toeplitz matrix `S_h`, vì đó là cách viết ma trận của một phép conv 1D. Khi đó, Hyena có dạng xen kẽ `D_x` và `S_h`."

Sau đó chỉ vào dòng minh họa và nói: "Điểm khác biệt lớn là attention tạo ra một ma trận dense `A(x)` kích thước `L x L`, còn Hyena thay nó bằng một chuỗi các phép nhân có cấu trúc. `D_x` rẻ vì là diagonal, `S_h` rẻ hơn vì có thể tính bằng FFT. Nhưng do vẫn có `D_x`, operator này vẫn phụ thuộc input, chứ không phải một conv cố định."

Nếu thầy hỏi sâu hơn, câu trả lời an toàn là: "`D_x` rẻ vì là ma trận đường chéo, còn `S_h` có cấu trúc convolution nên có thể tính nhanh bằng FFT."

Nếu người nghe bị ngợp, chỉ cần chốt một câu: "Hyena thay ma trận attention dày đặc bằng chuỗi các phép nhân có cấu trúc."
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
Slide này giải thích một điểm rất hay của paper: filter dài nhưng không cần học trực tiếp hàng nghìn hay hàng chục nghìn tham số cho từng vị trí.

Em có thể nói: "Nếu học filter theo cách explicit, nghĩa là lưu thẳng `h[0], h[1], ..., h[L-1]`, thì sequence càng dài, filter càng dài, và tham số sẽ tăng theo `L`. Paper tránh điều đó bằng cách học một hàm sinh filter."

Tiếp theo công thức: "Cụ thể, tại mỗi vị trí `t`, mô hình đưa positional encoding của `t` qua một FFN nhỏ để sinh ra giá trị filter `h_t`. Sau đó, một hàm window hoặc decay được nhân vào để giúp filter ổn định hơn, đặc biệt ở khoảng cách xa."

Ẩn dụ dễ nói là: "Thay vì học từng điểm của filter, mô hình học một công thức để sinh ra cả filter."

Chốt ý thật rõ: "Nhờ vậy, Hyena có thể có filter rất dài phù hợp với long-context, nhưng số tham số không cần nổ theo độ dài chuỗi. Đây là một trong những điểm tinh tế nhất của paper."
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
Đây là slide nói về hiện thực hiệu quả. Ở đây em nên tránh lao vào lý thuyết Fourier quá sâu. Điều quan trọng là người nghe hiểu ý tưởng đổi miền để biến convolution thành phép nhân và nhờ đó tính nhanh hơn.

Em có thể nói: "Long convolution nghe hợp lý về mặt ý tưởng, nhưng nếu tính trực tiếp thì vẫn tốn kém khi filter rất dài. Vì vậy Hyena dùng FFT convolution. Ý tưởng là đưa filter và signal sang miền tần số, khi đó phép convolution trong miền thời gian trở thành phép nhân element-wise trong miền tần số. Sau khi nhân xong, ta dùng inverse FFT để quay về lại output trên sequence."

Đi qua ba bước trên slide: "Bước 1 là FFT của `h` và `u`. Bước 2 là nhân từng phần tử trong miền tần số. Bước 3 là iFFT để lấy output trở lại. Chính nhờ cấu trúc này mà chi phí giảm xuống gần `O(L log L)`."

Nếu muốn gắn với code, nói thêm: "Trong repo, logic này nằm trong `HyenaOperator._causal_fft_conv`. Ở mức code, mình sẽ thấy `rfft`, nhân `H * V`, rồi `irfft` và cắt về độ dài `L` cần thiết."

Nếu bị hỏi vì sao không luôn nhanh hơn attention, trả lời: "FFT có overhead, nên ở `L` nhỏ lợi thế chưa chắc lộ rõ. Điểm mạnh của nó nằm ở context dài."

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
Đây là slide để kết nối method với lý do tại sao paper quan tâm đến Hyena cho bài toán long-context. Ở đây em nên nói cân bằng: không thần thánh hóa Hyena, nhưng cũng phải làm rõ điểm mạnh thực sự của nó.

Em có thể nói: "Nếu so sánh ở mức complexity, standard attention có time và memory `O(L^2)`. FlashAttention cải thiện cách truy cập memory và tối ưu thực thi rất giỏi, nhưng về mặt compute bản chất vẫn là `O(L^2)`. Còn Hyena có độ phức tạp xấp xỉ `O(N * L log L)`, trong đó `N` là order. Vì vậy, khi `L` tăng rất lớn, tốc độ tăng của Hyena chậm hơn attention."

Sau đó đưa ví dụ trực giác: "Ví dụ nếu `L = 1K`, thì `L^2` đã vào khoảng một triệu, còn `L log L` chỉ ở mức hàng chục nghìn. Khi lên `8K` hay `64K`, khoảng cách này càng rõ hơn."

Chốt thật rõ: "Paper không nói Hyena luôn nhanh hơn trong mọi tình huống. Ở sequence ngắn, overhead FFT và implementation có thể làm nó chưa vượt trội. Nhưng khi độ dài chuỗi tăng lên, lợi thế complexity mới bắt đầu thể hiện rõ."

Nếu muốn nối sang ý vì sao paper này đáng chú ý, nói thêm: "Chỗ đáng giá là paper không chỉ nói về tốc độ, mà còn cố thu hẹp quality gap với Transformer. Tức là họ không đánh đổi hoàn toàn chất lượng để lấy scaling."

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
Đây là slide tổng hợp xem paper gốc đã chứng minh được gì. Rất quan trọng là tách bạch giữa kết quả của paper và kết quả reproduction của nhóm.

Em có thể nói: "Đến đây, mình đã trình bày cơ chế. Câu hỏi tiếp theo là: paper gốc có chứng minh được gì không? Câu trả lời là có, trên hai mặt. Về quality, Hyena đạt kết quả gần với Transformer trên các benchmark language modeling như WikiText-103 và The Pile, đồng thời làm tốt trên một số bài synthetic có yêu cầu phụ thuộc dài. Về efficiency, khi sequence length tăng, Hyena cho thấy lợi thế runtime rõ ràng hơn attention, và trong paper thì ở mức 64K, tác giả báo cáo speedup rất lớn."

Sau đó nhấn mạnh ranh giới: "Đây là kết quả của paper gốc ở quy mô lớn, không phải reproduction của nhóm. Vì vậy mình không nên đồng nhất phần này với kết quả thực nghiệm sau đó."

Nếu bị hỏi vì sao bài này đáng chú ý hoặc vì sao được đăng, có thể trả lời: "Cái hay của bài không chỉ nằm ở việc chạy nhanh hơn, mà ở chỗ họ đề xuất một operator mới thay attention, chứ không chỉ sửa attention cũ. Họ kết hợp long convolution, data-controlled gating và implicit filter thành một kiến trúc attention-free vẫn đủ mạnh cho language modeling. Vì vậy bài có cả ý tưởng mới, lý do lý thuyết rõ, và kết quả thực nghiệm đủ thuyết phục."

Kết thúc bằng câu chuyển sang TV3: "Các kết quả vừa rồi là của paper gốc ở quy mô lớn. Trong phạm vi môn học, nhóm sẽ reproduction nhỏ hơn trên WikiText-2 để kiểm tra xu hướng, chứ không claim đạt lại toàn bộ con số của paper."
-->

---

<!-- _class: lead -->

# Chuyển Sang Reproduction

Các kết quả vừa rồi là của paper gốc ở quy mô lớn.

Trong phạm vi môn học, nhóm thu nhỏ bài toán để kiểm chứng xu hướng trên WikiText-2 với Transformer-small và Hyena-small.

<!--
Notes:
Nếu giữ slide này, nó đóng vai trò câu nối rất đẹp giữa TV2 và TV3.

Em có thể nói: "Tất cả các kết quả ở slide trước là của paper gốc ở quy mô lớn. Còn trong phạm vi môn học, nhóm không nhằm tái hiện toàn bộ benchmark đó, mà thu nhỏ bài toán lại: model nhỏ hơn, sequence ngắn hơn, benchmark gọn hơn. Mục tiêu của reproduction không phải là đạt đúng từng con số của paper, mà là kiểm tra xem xu hướng chính có còn giữ được hay không."

Sau đó chuyển người nói: "Sau đây, Quang sẽ trình bày phần reproduction của nhóm."
-->
