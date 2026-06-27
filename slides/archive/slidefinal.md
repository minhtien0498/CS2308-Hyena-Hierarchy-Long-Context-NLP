---
marp: true
title: "Hyena Hierarchy — Towards Larger Convolutional Language Models"
author: "Trần Tú Quang · Tô Huỳnh Minh Tiến · Kiên (Nhóm 08)"
paginate: true
html: true
math: katex
backgroundColor: "#ffffff"
color: "#1d2b36"
# ============================================================
#  MARP TEMPLATE — theme UIT (primary navy #1F3A68)
#   - Slide nội dung: dùng `## ...` (ra THANH NAVY tràn viền)
#   - Slide bìa: <!-- _class: lead --> + <div class="titlebox">
#   - Slide chuyển mục: <!-- _class: lead --> + `# ...`
#   - Slide cảm ơn: <!-- _class: lead --> + <div class="thanks">
# ============================================================
style: |
  @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,400;0,600;0,700;1,400&display=swap');
  :root {
    --navy:#1F3A68;
    --navy-deep:#16294d;
    --ink:#1d2b36;
    --accent:#2a6df4;
    --soft:#eef3fb;
    --line:#d4deee;
    --muted:#6b7a90;
  }
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
  .caption { font-size:16px; color:#888; font-style:italic; }
  .cols { display:flex; gap:30px; }
  .col { flex:1; }
  .box { background:#e7edf6; border:1px solid #c3d2ea; border-radius:10px; padding:12px 20px; }
  .diagram { text-align:center; margin-top:14px; }
  .diagram img { max-height:300px; width:auto; }
  p { margin: 9px 0; }
  .katex-display {
    background: linear-gradient(180deg, #f7faff 0%, #eef3fb 100%);
    border: 1px solid var(--line);
    border-left: 5px solid var(--navy);
    border-radius: 12px;
    padding: 16px 22px;
    margin: 14px 0;
    box-shadow: 0 2px 12px rgba(15,29,56,.07);
  }
  .katex { font-size: 1.18em; }
  pre {
    background: #f7faff;
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 14px 18px;
    box-shadow: 0 2px 12px rgba(15,29,56,.06);
  }
  pre code {
    background: none;
    color: #20324f;
    font-size: 19px;
    line-height: 1.6;
  }
  .warn {
    background:#fff8ec;
    border:1px solid #f3dca6;
    border-left:5px solid #e0a51e;
    border-radius:0 12px 12px 0;
    padding:13px 22px;
  }
  .grid2 { display:grid; grid-template-columns:1fr 1fr; gap:20px; align-items:start; }
  .center { text-align:center; }
  .yes { color:#15803d; font-weight:700; }
  .no  { color:#b04a4a; font-weight:700; }
  .flow { display:flex; flex-direction:column; align-items:center; gap:5px; margin:14px 0; }
  .flow .step {
    background:#fff;
    border:1.5px solid #cdd9ec;
    border-radius:10px;
    padding:9px 22px;
    font-weight:600;
    color:var(--navy);
    font-size:21px;
    box-shadow:0 2px 8px rgba(15,29,56,.06);
  }
  .flow .step.fill { background:var(--navy); color:#fff; border-color:var(--navy); }
  .flow .ar { color:var(--accent); font-size:17px; line-height:1; }
  .chips { display:flex; flex-wrap:wrap; align-items:center; gap:7px; justify-content:center; margin:8px 0 4px; }
  .chip {
    background:var(--navy);
    color:#fff;
    border-radius:999px;
    padding:6px 15px;
    font-size:18px;
    font-weight:600;
  }
  .chip.alt { background:#eef3fb; color:var(--navy); border:1px solid #cdd9ec; }
  .chip.hot { background:linear-gradient(135deg,var(--navy),var(--accent)); }
  .sep { color:#9bb0cf; font-weight:700; }
  .mono {
    background:#0f1f3d;
    color:#dbe7ff;
    border-radius:12px;
    padding:16px 22px;
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    font-size:19px;
    line-height:1.55;
    box-shadow:0 4px 16px rgba(15,29,56,.22);
    display:inline-block;
  }
  .mono .dim { color:#7f93bd; }
  .tight table { font-size:18.5px; }
footer: '<span>Nhóm 08 · CS2308</span><span>Hyena Hierarchy (ICML 2023)</span><span>2026</span><span></span>'
header: '<img src="assets/UIT_logo.svg" alt="UIT">'
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

<span class="small">GVHD: TS. Nguyễn Văn Kiệt · University of Information Technology, VNU-HCM (UIT) · 2026</span>

---

## Nội dung trình bày

I. **Câu hỏi nghiên cứu và động lực**
II. **Nền tảng**: Language Modeling, Transformer, Self-Attention, nút thắt $O(L^2)$
III. **Khoảng cách năng lực và related work**
IV. **Cơ chế Hyena**: long convolution, gating, recurrence, hierarchy
V. **Hiện thực hiệu quả**: matrix view, implicit filter, FFTConv, complexity
VI. **Kết quả paper gốc và reproduction của nhóm**

---

<!-- _class: lead -->

# I. Câu hỏi nghiên cứu và động lực

---

## 1. Câu hỏi nghiên cứu và động lực

### "Is attention all we need?"

- Self-attention là **trái tim** của Transformer và tạo nên hầu hết thành công của nó.
- Nhưng attention có **chi phí bậc hai** $O(L^2)$ theo độ dài chuỗi $L$ → đặt **giới hạn cứng** lên lượng ngữ cảnh.
- Các toán tử dưới-bậc-hai trước đây (Linformer, Reformer, Performer, sparse…) đều phải **lai ghép** với attention dày đặc mới đạt chất lượng.

<div class="box">

**Câu hỏi trung tâm (paper · Section 1):**
*“Are there subquadratic operators that, inspired by its properties, are able to match its quality at scale?”*

</div>

→ Mục tiêu: toán tử **không-attention**, rẻ hơn, **không cần hybridization**, vẫn sánh ngang Transformer.

<!--
Notes:
"Hook" của cả bài. Đọc to câu hỏi nghiên cứu. Nhấn: paper không xấp xỉ attention mà hỏi liệu có operator KHÁC thay được không.
-->

---

<!-- _class: lead -->

# II. Nền tảng

---

## 2. Vì sao long-context quan trọng?

- Nhiều bài toán thực tế cần **ngữ cảnh dài**: cả cuốn sách, mã nguồn dài, hội thoại dài, văn bản luật.
- Ngoài ngôn ngữ: **chuỗi sinh học (DNA / protein)**, âm thanh dài, ảnh gigapixel.
- Nhưng $L$ tăng → attention tăng chi phí theo $L^2$ → nhanh chóng **hết bộ nhớ (OOM)** và **chậm**.

<div class="box">

"Phá vỡ rào cản bậc hai" mở ra: dùng cả textbook làm ngữ cảnh, sinh nhạc dài, xử lý ảnh cực lớn *(paper · Section 1)*.

</div>

<!--
Notes:
Cho 2-3 ví dụ cụ thể để khán giả thấy long-context không phải nhu cầu lý thuyết. Đây là động lực để tìm operator rẻ hơn.
-->

---

## 3. Nhắc lại: Language Modeling & Perplexity

**Autoregressive LM** — dự đoán token kế tiếp:

$$
P(w_1,\dots,w_n)=\prod_{t=1}^{n} P\!\left(w_t \mid w_{<t}\right)
$$

**Perplexity** — thước đo chất lượng LM (càng **thấp** càng tốt):

$$
\mathrm{PPL}=\exp\!\left(-\frac{1}{N}\sum_{t=1}^{N}\log P\!\left(w_t \mid w_{<t}\right)\right)=\exp(\text{loss})
$$

<span class="small">Trong PyTorch: PPL = exp(validation cross-entropy). Đây cũng là metric nhóm dùng ở phần thực nghiệm (Quang).</span>

<!--
Notes:
Giữ gọn. Khán giả chỉ cần nhớ: PPL thấp = đoán token tốt hơn. Cầu nối tới kết quả perplexity của paper và phần reproduction.
-->

---

## 4. Nhắc lại kiến trúc Transformer

<div class="flow">
<div class="step">Tokens</div>
<div class="ar">▼</div>
<div class="step">Token Embedding &nbsp;+&nbsp; Positional Embedding</div>
<div class="ar">▼</div>
<div class="step fill">N × Transformer Block</div>
<div class="ar">▼</div>
<div class="step">LayerNorm &nbsp;→&nbsp; LM Head &nbsp;→&nbsp; logits</div>
</div>

**Một Transformer Block** (Pre-LN + residual):

$$
\begin{aligned}
\mathbf{x} &\;\leftarrow\; \mathbf{x} + \mathrm{MHA}\!\big(\mathrm{LN}(\mathbf{x})\big)\\[2pt]
\mathbf{x} &\;\leftarrow\; \mathbf{x} + \mathrm{FFN}\!\big(\mathrm{LN}(\mathbf{x})\big)
\end{aligned}
$$

→ **Self-Attention** là phép *trộn thông tin* giữa các token — và cũng chính là **nút thắt** ta cần phân tích.

<!--
Notes:
Định vị attention trong block. FFN xử lý theo từng vị trí; attention mới là phần trộn token-token (tốn O(L^2)).
-->

---

## 5. Self-Attention hoạt động thế nào

$$
\mathrm{Attention}(Q,K,V)=\mathrm{SoftMax}\!\left(\frac{QK^{\top}}{\sqrt{d_k}}\right)V
$$

- **B1.** Chiếu tuyến tính: $Q=XW_Q,\quad K=XW_K,\quad V=XW_V$.
- **B2.** Điểm tương quan: $S=QK^{\top}/\sqrt{d_k}$ → ma trận $L\times L$.
- **B3.** Causal mask + SoftMax theo hàng → trọng số $A$.
- **B4.** Tổng có trọng số: $\mathrm{Output}=A\,V$.

<span class="small">Multi-Head: chạy nhiều phép attention song song với các $W_Q,W_K,W_V$ khác nhau, rồi nối lại.</span>

<!--
Notes:
Ẩn dụ truy vấn–khóa–giá trị. Nhấn: bước B2 tạo ma trận L×L — gốc rễ của O(L^2). Dẫn sang slide ma trận attention.
-->

---

## 6. Ma trận Attention & Causal Mask

<div class="grid2">
<div>

- Mỗi token tính tương quan với **mọi token** → ma trận $L\times L$.
- **Causal LM:** token tại $t$ chỉ "nhìn" $t'\le t$ → mask **tam giác dưới** ($-\infty$ ở tương lai, sau SoftMax $=0$).
- Số ô cần tính/lưu tỉ lệ với $L^2$.

</div>
<div class="center">

<div class="mono">
&nbsp;&nbsp;&nbsp;&nbsp;k0&nbsp;k1&nbsp;k2&nbsp;k3<br>
q0&nbsp;[&nbsp;●&nbsp;&nbsp;<span class="dim">·</span>&nbsp;&nbsp;<span class="dim">·</span>&nbsp;&nbsp;<span class="dim">·</span>&nbsp;]<br>
q1&nbsp;[&nbsp;●&nbsp;&nbsp;●&nbsp;&nbsp;<span class="dim">·</span>&nbsp;&nbsp;<span class="dim">·</span>&nbsp;]<br>
q2&nbsp;[&nbsp;●&nbsp;&nbsp;●&nbsp;&nbsp;●&nbsp;&nbsp;<span class="dim">·</span>&nbsp;]<br>
q3&nbsp;[&nbsp;●&nbsp;&nbsp;●&nbsp;&nbsp;●&nbsp;&nbsp;●&nbsp;]
</div>

<span class="small">● attend (quá khứ) · <span class="dim">·</span> bị mask</span>

</div>
</div>

→ Đây là lý do attention **không mở rộng** được khi $L$ rất lớn.

<!--
Notes:
Dùng hình tam giác để khán giả "thấy" vì sao chi phí là L×L. Nối sang slide O(L^2).
-->

---

## 7. Nút thắt $O(L^2)$

<div class="grid2">
<div>

| $L$ | Số ô $L^2$ | $L$ tăng 2× |
|---|---|---|
| 256 | 65,536 | — |
| 512 | 262,144 | ~4× |
| 1,024 | 1,048,576 | ~4× |
| 8,192 | 67,108,864 | ~4× |
| 64,000 | ~4.1 × 10⁹ | → **OOM** |

</div>
<div>

- **Thời gian:** $QK^{\top}$, SoftMax, $AV$ đều $\sim O(L^2 d)$ mỗi lớp.
- **Bộ nhớ:** lưu ma trận $L\times L$ cho backprop $\Rightarrow O(L^2)$.

<div class="box">

$L$ tăng **2×** → chi phí tăng **~4×**. Đây là rào cản chính cần phá vỡ.

</div>

</div>
</div>

<!--
Notes:
Slide "đinh" của TV1. Để khán giả nhìn bảng và tự thấy độ tăng bậc hai. Câu chốt: gấp đôi độ dài thì gấp bốn chi phí.
-->

---

## 8. FlashAttention có giải quyết triệt để?

- **FlashAttention** (Dao et al., 2022) tối ưu **truy cập bộ nhớ (IO-aware)**: không vật chất hóa toàn bộ ma trận $L\times L$, tính theo khối trên SRAM.
- → Giảm mạnh **bộ nhớ thực tế**, nhanh hơn 2–4× so với attention thường.

<div class="warn">

**Nhưng:** số phép tính vẫn là $O(L^2)$ — FlashAttention tối ưu *cách chạy*, không đổi *độ phức tạp*. Vẫn khó vươn tới ngữ cảnh cực dài.

</div>

→ Cần một toán tử có **độ phức tạp dưới bậc hai** thật sự, không chỉ tối ưu hằng số.

<!--
Notes:
Câu này hay bị thầy hỏi → nói rõ: FlashAttention là kỹ thuật cài đặt (IO-aware), compute vẫn O(L^2). Đây là lý do paper Hyena vẫn cần thiết.
-->

---

<!-- _class: lead -->

# III. Khoảng cách năng lực và related work

---

## 9. Khoảng cách năng lực (Capability Gap)

Vì sao các toán tử rẻ trước đây **thua** attention? Paper dùng **mechanistic interpretability** để rút ra **3 năng lực** cần giữ:

| Năng lực | SSM / Conv tĩnh | Attention |
|---|---|---|
| **Data control** — phụ thuộc dữ liệu | <span class="no">Không</span> (tĩnh) | <span class="yes">Có</span> — $A(u)$ |
| **Unrestricted context** — ngữ cảnh không giới hạn | <span class="no">Không</span> (bị locality) | <span class="yes">Có</span> |
| **Sublinear params** — tham số ⟂ độ dài chuỗi | <span class="yes">Có</span> | <span class="yes">Có</span> |

<div class="box">

Hyena được thiết kế để **giữ đồng thời cả ba** — thay vì *xấp xỉ* attention, ta *tái dựng* tính chất của nó bằng primitive rẻ hơn.

</div>

<!--
Notes:
3 tính chất này là bản lề bàn giao sang Tiến (TV2): long convolution + gating dựng lại đúng 3 tính chất này.
-->

---

<!-- _class: tight -->

## 10. Related Work — Hyena nằm ở đâu?

<div class="chips">
<span class="chip alt">Attention 2017</span><span class="sep">→</span>
<span class="chip alt">SSM</span><span class="sep">→</span>
<span class="chip alt">S4 2021</span><span class="sep">→</span>
<span class="chip alt">H3 / GSS 2022</span><span class="sep">→</span>
<span class="chip hot">Hyena 2023</span><span class="sep">→</span>
<span class="chip alt">Mamba ’23</span>
</div>

| Kiến trúc | Phép trộn | Gating | Train | Ghi chú |
|---|---|---|---|---|
| Transformer | Attention | — | $O(L^2)$ | đầy đủ ngữ cảnh, nghẽn $L^2$ |
| S4 | SSM (conv) | Không | $O(L\log L)$ | học phụ thuộc dài, thiếu data-control |
| H3 / GSS | SSM (conv) | Có | $O(L\log L)$ | attention-free đầu tiên sánh Transformer 125M |
| **Hyena** | **Implicit long conv** | Có (recurrence bậc N) | $O(N\,L\log L)$ | **tổng quát hóa H3/GSS**, filter tự do |
| Mamba | Selective SSM | Có | $O(L)$ | ra **sau** Hyena, filter động theo input |

<span class="small">Hyena bậc 2 ⟺ H3 · Hyena bậc 1 ⟺ GSS. "Hierarchy" = họ toán tử có thứ bậc, mô hình cũ là tầng thấp.</span>

<!--
Notes:
Không đi sâu toán. Khán giả thấy "dòng chảy" tiến hóa và vị trí Hyena. Mamba để sau Hyena, nhắc nhẹ để không hiểu nhầm thứ tự thời gian.

★ CÂU CHỐT & BÀN GIAO — đọc miệng khi kết thúc slide này (không cần slide riêng):
"Như vậy, ta đã thấy Attention rất mạnh nhưng vướng chi phí O(L²) khi chuỗi dài, và đã rút ra ba năng lực cốt lõi cần giữ lại: phụ thuộc dữ liệu (data control), ngữ cảnh không giới hạn, và số tham số độc lập với độ dài chuỗi. Câu hỏi đặt ra cho phần tiếp theo là: làm sao dựng lại đúng ba năng lực đó bằng một toán tử rẻ hơn? Mời Tiến trình bày cơ chế Hyena — long convolution kết hợp gating, tính hiệu quả qua FFTConv."
-->

---

<!-- _class: lead -->

# IV. Cơ chế Hyena

---

## 11. Từ Attention Sang Hyena

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

## 12. Ý Tưởng Chính Của Hyena

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

## 13. Long Convolution

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

## 14. Data-Controlled Gating

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

## 15. Hyena Recurrence

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

## 16. Order-N Hierarchy

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

<!-- _class: lead -->

# V. Hiện thực hiệu quả

---

## 17. Matrix View

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

## 18. Implicit Filter

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

## 19. FFTConv

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

## 20. Complexity Và Ý Nghĩa

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

<!-- _class: lead -->

# VI. Kết quả paper gốc và reproduction của nhóm

---

## 21. Kết quả paper gốc và reproduction của nhóm

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

---

## 22. Bối cảnh & Động lực

### Vì sao cần thay thế attention?

- Self-attention là trái tim của Transformer, nhưng có **chi phí bậc hai O(L²)** theo độ dài chuỗi `L`.
- Chi phí này đặt **giới hạn cứng** lên lượng ngữ cảnh: khó dùng cả sách, nhạc dài, ảnh gigapixel, chuỗi DNA.
- Các giải pháp dưới bậc hai hiện có (Linformer, Reformer, Performer, sparse…) đều **phải lai ghép** với attention dày đặc mới đạt chất lượng, nên vẫn tồn tại **capability gap**.

<div class="box">

**Câu hỏi nghiên cứu trung tâm:**
*“Is attention all we need? Are there subquadratic operators that, inspired by its properties, are able to match its quality at scale?”*

</div>

Mục tiêu: một toán tử **không dùng attention**, rẻ hơn, **không cần lai ghép**, vẫn sánh ngang Transformer ở quy mô lớn.

---

## 23. Khoảng cách năng lực (capability gap)

Vì sao các toán tử rẻ trước đây thua attention? Nhóm tác giả dùng **mechanistic interpretability** để truy ra 3 năng lực mấu chốt mà chúng thiếu:

| Năng lực | SSM / Conv cố định | Attention |
|---|---|---|
| Phụ thuộc dữ liệu (data control) | Không, tĩnh | Có, `A(u)` |
| Ngữ cảnh không giới hạn | Không, thường bị locality | Có |
| Số tham số độc lập độ dài chuỗi | Có | Có |

Hyena được thiết kế để **giữ đồng thời cả ba**: thay vì xấp xỉ attention, nhóm tác giả tái dựng các tính chất của nó bằng primitive rẻ hơn.

---

## 24. Định nghĩa bài toán

### Ba thuộc tính cần bảo toàn

Phân rã self-attention: $y = A(q,k)\,v$, với $A(u)=\mathrm{SoftMax}\!\big(\tfrac{1}{\sqrt D}\,uM_q M_k^\top u^\top\big)$.

1. **Data control**: `A(u)` là toán tử tuyến tính *do dữ liệu quyết định*, một khối mã hóa cả họ hàm tuyến tính.
2. **Sublinear parameter scaling**: số tham số **tách rời** độ dài chuỗi, nhờ vậy dồn được tham số vào FFN.
3. **Unrestricted context**: không áp đặt locality, cho phép phụ thuộc tầm xa giữa bất kỳ hai vị trí.

<div class="box">

**Ý tưởng Hyena:** thay vì xấp xỉ ma trận attention, hãy xây một toán tử **data-controlled** mới từ hai primitive rẻ: **long convolution** + **element-wise gating**.

</div>

---

## 25. Định nghĩa toán tử Hyena (bậc N)

Cho `N+1` phép chiếu tuyến tính của đầu vào $(v, x^1,\dots,x^N)$ và `N` bộ lọc dài học được $h^1,\dots,h^N$:

$$
\begin{aligned}
z_t^{1} &= v_t \\
z_t^{n+1} &= x_t^{n}\,\big(h^{n} * z^{n}\big)_t, \quad n=1,\dots,N \\
y_t &= z_t^{N+1}
\end{aligned}
$$

- $x_t^n$ là **gate** phụ thuộc đầu vào (nhân element-wise).
- $h^n * z^n$ là **long convolution** (bộ lọc dài bằng cả chuỗi).
- Khác attention: số phép chiếu **không bắt buộc bằng 3**; chiều sâu `N` của recurrence là siêu tham số điều khiển bậc của toán tử.

<span class="small">Short recurrences thu được các mô hình cũ (H3, GSS) như trường hợp đặc biệt.</span>

<div class="diagram">

![h:240px](../docs/images/fig1_hyena_hierarchy.png)

</div>

---

## 26. Đào sâu toán học

### Từ recurrence sang dạng ma trận

Recurrence Hyena viết lại được dưới dạng **tích các ma trận data-controlled**:

$$
y = H(u)\,v = D_x^{N}\,S_h^{N}\,\cdots\,D_x^{2}\,S_h^{2}\,D_x^{1}\,S_h^{1}\,v
$$

- $D_x^{n} = \mathrm{diag}(x^{n}) \in \mathbb{R}^{L\times L}$ là ma trận **đường chéo** (chính là gating).
- $S_h^{n} \in \mathbb{R}^{L\times L}$ là ma trận **Toeplitz** sinh bởi bộ lọc $h^n$ (chính là convolution).

> So sánh trực quan (Figure 2): SelfAttention $y=A(q,k)v$ là **một** ma trận dày data-controlled; còn Hyena là **tích xen kẽ** của đường chéo và Toeplitz, một phân rã thưa nhưng vẫn data-controlled, lấy cảm hứng từ *butterfly decomposition*.

<div class="diagram">

![h:240px](../docs/images/fig2_matrix_view.png)

</div>

---

## 27. Vì sao Hyena tổng quát hóa H3 & GSS

H3 (Dao et al.) thực ra là một phân rã 3 thừa số:

$$
A(q,k) = D_q\, S_\psi\, D_k\, S_\varphi, \qquad H3(q,k,v)=A(q,k)v
$$

- **Hyena bậc 2** tương đương cơ chế **H3**.
- **Hyena bậc 1** tương đương **GSS**, với một cách tham số hóa cụ thể cho bộ lọc (qua SSM).
- Hyena tổng quát hóa lên **bậc N tùy ý** và bộ lọc **dạng tự do (free-form)** thay vì buộc qua SSM.

Đây chính là ý nghĩa "hierarchy": một họ toán tử có thứ bậc, các mô hình trước là tầng thấp.

---

## 28. FFTConv: tính convolution dài mà không vật chất hóa ma trận

Tính trực tiếp $S_h v$ tốn $O(L^2)$. Mẹo: **chéo hóa ma trận tuần hoàn bằng cơ sở Fourier**.

$$
\hat S_h = W^{-1} D_H\, W, \qquad D_H=\mathrm{diag}\big(\mathrm{FFT}(h)\big)
$$

$$
\boxed{\;\mathrm{pad}(y)=\mathrm{iFFT}\big(\mathrm{FFT}(\mathrm{pad}(h))\odot \mathrm{FFT}(\mathrm{pad}(u))\big)\;}
$$

- Zero-pad biến tích chập **tuyến tính** thành tích chập **vòng** (circular), tức nhân với ma trận tuần hoàn.
- Mỗi FFTConv tốn $O(L\log_2 L)$ và **không cần tạo ma trận $L\times L$ trong RAM**, nhờ vậy tránh tràn bộ nhớ (OOM).

---

## 29. Độ phức tạp & đối ngẫu miền thời gian/tần số

**Độ phức tạp toàn toán tử bậc N** (Proposition 3.2):

$$
\mathcal{O}\big(N\,D\,L\,(\log_2 L + D)\big) \;\ll\; \mathcal{O}(L^2)
$$

**Trực giác: đối ngẫu hai miền**
- *Convolution ở miền thời gian* tương đương *nhân element-wise ở miền tần số* (và ngược lại).
- Hyena **luân phiên** giữa convolution (mở rộng "memory", gom ngữ cảnh rộng) và gating (nhân element-wise để lựa chọn thành phần tần số tinh tế).

Sự đan xen này là một giả thuyết lý giải vì sao Hyena hiệu quả: vừa nhìn xa, vừa lọc chọn lọc.

---

## 30. Bộ lọc ngầm & tính nhân quả

Bộ lọc dài **không** học như một vector tham số khổng lồ, mà **sinh ra từ một FFN nhỏ** (implicit parametrization):

$$
h_t = \mathrm{Window}(t)\cdot\big(\mathrm{FFN}\circ \mathrm{PositionalEncoding}\big)(t)
$$

- **Tách rời** độ dài bộ lọc khỏi số tham số (sublinear scaling).
- `Window(t)=exp(-αt)` cho suy giảm mũ, điều hòa độ dài hiệu dụng; sine tần số cao trong FFN chống *low-frequency bias*.

**Proposition 3.1 (Causal Hyenas):** nếu mọi $h^n$ nhân quả thì toán tử Hyena nhân quả, nhờ vậy huấn luyện tự hồi quy được (như mask tam giác của Transformer).

---

## 31. Dữ liệu & Đánh giá

### Xây dựng dữ liệu

**(a) Synthetic, tự thiết kế để dò cơ chế** (làm khó bằng độ dài và từ vựng lớn):

| Tác vụ | Prompt | Target |
|---|---|---|
| Associative Recall | `a,1,b,e,3,f,b` | `e` |
| Majority | `a,g,g,g,e,f,g` | `g` |
| Counting | `a,b,b,b,a,c,b` | `4` |
| ICL of Functions | `x₀,f(x₀),…,xₙ` | `f(xₙ)` |
| Arithmetic | `1,3,5,+,6,8,3` | `8,1,8` |

Associative Recall đẩy tới **131k token** (lần đầu trình diễn ICL ở độ dài này).

**(b) Benchmark chuẩn**: WikiText103, **The Pile (800GB)**, SuperGLUE, ImageNet-1k, CIFAR.

---

## 32. Các phương pháp đánh giá

| Chiều | Cách đo | Kết quả |
|---|---|---|
| Năng lực cơ chế | Acc.% trên synthetic | **Duy nhất** giải được recall; **+>50đ** vs SSM |
| Mô hình ngôn ngữ | **Perplexity** (WT103, Pile) | = Transformer, **không hybrid** |
| Hiệu quả | **FLOPs**, scaling law | đạt GPT với **−20% FLOPs** |
| Tốc độ | runtime (ms) | **2×** @8K, **100×** @64K |
| Downstream | SuperGLUE, few-shot | sánh RWKV, ít token hơn |
| Thị giác | Acc. ImageNet/CIFAR | Hyena-ViT = ViT; Hyena-ISO **91.2%** |

<span class="small">Hyena bắt kịp attention tại L≈2048, bắt kịp FlashAttention tại L≈4096 đến 8192.</span>

---

## 33. Kết quả & Ảnh hưởng

### Tác động của nghiên cứu

- **Thách thức "attention is all you need":** kiến trúc dưới bậc hai, đơn giản hơn, *có thể* sánh ngang Transformer ở quy mô dưới 1 tỷ tham số, dẫn tới nhận định *“attention may not be all we need.”*
- **Mở đường ngữ cảnh siêu dài:** Hyena là nền cho **HyenaDNA, Evo** (bộ gene, chuỗi 10⁵ đến 10⁶ token) và **StripedHyena**, cộng hưởng với dòng **SSM, Mamba** ở những nơi attention bất khả thi.
- **Diễn giải cơ chế thành công cụ thiết kế:** benchmark recall và induction trở thành la bàn thiết kế kiến trúc, không chỉ để chấm điểm.
- **Primitive tổng quát:** dùng được ngoài ngôn ngữ, cho cả ảnh, âm thanh, sinh học.

> Thông điệp kết: hiểu *vì sao* attention mạnh quan trọng hơn việc *sao chép* attention.

---

## 34. Thực nghiệm

### Phạm vi & mục tiêu

Nhóm không tái hiện toàn bộ paper, vì The Pile 800GB và GPU lớn vượt quá tài nguyên môn học. Thay vào đó nhóm làm tái hiện ở quy mô nhỏ, mục tiêu là kiểm chứng xu hướng chứ không khớp số tuyệt đối.

<div class="box">

Hai câu hỏi nhóm muốn tự trả lời:
1. Ở quy mô nhỏ, perplexity của Hyena có ngang Transformer không?
2. Khi chuỗi dài ra, Hyena có lợi thế tốc độ như paper dự đoán không?

</div>

Code do nhóm tự cài bằng thuần PyTorch, có đối chiếu với bản chính chủ `HazyResearch/safari`.

---

## 35. Thiết lập thực nghiệm

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

## 36. Kết quả E1: Perplexity (L=256)

| Model | Val loss | Val PPL |
|---|---|---|
| Transformer-small | 5.69 | 295.6 |
| Hyena-small | 5.53 | 251.8 |

<span class="small">Kết quả sơ bộ sau 5 epoch, chạy bằng notebook <code>notebooks/colab_E1_run.ipynb</code>. Loss vẫn đang giảm nên đây là số minh hoạ xu hướng, chưa phải mức hội tụ cuối.</span>

Nhận xét: hai model cùng cỡ tham số cho perplexity cùng tầm, Hyena còn nhỉnh hơn một chút. Đủ để nói Hyena là một baseline ngôn ngữ hợp lệ ở quy mô này.

---

## 37. Kết quả: tốc độ theo độ dài chuỗi

Đo thời gian forward với input giả, cùng cấu hình model 16M tham số, batch 8, trên Colab T4. Tăng dần độ dài L:

| L | Transformer (ms) | Hyena (ms) | Tỉ lệ |
|---|---|---|---|
| 256 | 21.4 | 21.9 | Hyena chậm hơn chút |
| 512 | 43.7 | 42.4 | hai bên hòa nhau |
| 1024 | 100.1 | 84.1 | Hyena nhanh hơn ~1.19 lần |

Ở L=2048 Hyena vẫn chạy tốt (khoảng 168 ms) trong khi Transformer bắt đầu đuối. Attention tăng theo bình phương độ dài, còn Hyena tăng gần tuyến tính, nên chuỗi càng dài Hyena càng lợi.

---

## 38. Thảo luận và giới hạn

- Ở chuỗi ngắn Hyena chậm hơn, vì chi phí FFT và đệm 2L lớn hơn phần tiết kiệm được. Hyena hòa ở khoảng L bằng 512 và vượt lên từ L bằng 1024, đúng như lưu ý trong paper.
- Bản cài của nhóm có đơn giản hóa so với safari: filter dùng SiLU thay cho activation dạng sin, modulation rút gọn, bỏ skip-connection. Vì vậy hội tụ có thể chậm hơn bản gốc.
- Vì dùng thuần PyTorch và không có CUDA kernel, nhóm chưa đạt mức speedup tuyệt đối như paper.
- Phần đo tốc độ dùng input giả để đo thời gian forward, không phải đánh giá perplexity trên tập validation.
- Cần phân biệt rõ: số trên WikiText-103, The Pile và speedup từ 8K đến 64K là của paper gốc, còn số WikiText-2 ở đây là của nhóm.

---

## 39. Kết luận phần tái hiện

- Nhóm tự cài Hyena bằng thuần PyTorch, phần lõi khớp với bản chính chủ ở FFTConv đệm 2L, short conv depthwise và gating đệ quy bậc N.
- Quan sát đúng xu hướng chính của bài: tốc độ Hyena tăng gần tuyến tính, attention tăng theo bình phương, hai đường giao nhau quanh L bằng 512 và Hyena vượt lên rõ từ L bằng 1024.
- Bài học rút ra: hiểu được vì sao attention nghẽn ở chuỗi dài, và thấy được giới hạn thực tế của tái hiện khi thiếu kernel tối ưu và tài nguyên.

> Quy mô nhỏ nhưng đủ để thấy tận mắt cơ chế dưới bậc hai mà bài báo đề xuất.

---

<!-- _class: lead -->

<div class="thanks">

# Cảm ơn! · Q&A

</div>

**Nhóm 08 · CS2308**
Trần Tú Quang · Tô Huỳnh Minh Tiến · Kiên

<span class="small">Tài liệu: Poli et al., *Hyena Hierarchy*, ICML 2023 · docs/poli23a.pdf
Tài liệu nhóm: README.md · notebooks/colab_E1_run.ipynb</span>
