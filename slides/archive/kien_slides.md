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
  @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap');
  :root {
    --navy:#1F3A68; --navy-deep:#16294d; --ink:#1d2b36;
    --accent:#2a6df4; --soft:#eef3fb; --line:#d4deee; --muted:#6b7a90;
  }
  section {
    font-family: "Be Vietnam Pro", "Segoe UI", system-ui, sans-serif;
    font-size: 24px;
    padding: 96px 70px 60px 70px;
    background:
      radial-gradient(1200px 380px at 88% -8%, #eef3fb 0%, rgba(238,243,251,0) 60%),
      #ffffff;
    color: var(--ink);
    display: flex; flex-direction: column;
    justify-content: flex-start !important; align-content: flex-start;
    letter-spacing:.1px;
  }
  h2 {
    position: absolute; top: 0; left: 0; right: 0; margin: 0;
    background: linear-gradient(100deg, var(--navy-deep) 0%, var(--navy) 58%, #28508f 100%);
    color: #ffffff !important; font-size: 29px; font-weight: 600;
    padding: 18px 70px 16px 70px;
    box-shadow: 0 3px 14px rgba(15,29,56,.18);
  }
  h3 {
    color: var(--navy); font-size: 23px; font-weight: 700; margin: 2px 0 14px 0;
    padding-bottom: 7px; border-bottom: 2px solid var(--line); display: inline-block;
  }
  p { margin: 9px 0; }
  strong { color: var(--navy); font-weight: 700; }
  em { color: var(--accent); font-style: normal; font-weight: 600; }
  a { color: var(--navy); }
  code {
    background: var(--soft); color: var(--navy); padding: 1px 7px;
    border-radius: 5px; font-size: .94em;
  }
  ul { list-style: none; padding-left: 4px; margin: 8px 0; }
  ul li { position: relative; padding-left: 26px; margin: 12px 0; line-height: 1.45; }
  ul li::before {
    content: ""; position: absolute; left: 3px; top: .55em;
    width: 8px; height: 8px; border-radius: 3px;
    background: linear-gradient(135deg, var(--navy), var(--accent));
  }
  ol { padding-left: 22px; } ol li { margin: 11px 0; line-height: 1.45; }
  table { font-size: 21px; border-collapse: collapse; margin: 10px 0; width: 100%;
    box-shadow: 0 2px 10px rgba(15,29,56,.07); border-radius: 10px; overflow: hidden; }
  thead th { background: var(--navy); color: #fff; font-weight: 600; }
  tbody tr:nth-child(even) td { background: #f6f9fe; }
  td, th { border: 1px solid var(--line); padding: 8px 14px; }
  blockquote {
    border: none; border-left: 5px solid var(--accent);
    background: var(--soft); color: #20324f; padding: 12px 22px;
    border-radius: 0 12px 12px 0; margin: 12px 0;
  }
  /* ── Display math as an elegant card ── */
  .katex-display {
    background: linear-gradient(180deg, #f7faff 0%, #eef3fb 100%);
    border: 1px solid var(--line); border-left: 5px solid var(--navy);
    border-radius: 12px; padding: 16px 22px; margin: 14px 0;
    box-shadow: 0 2px 12px rgba(15,29,56,.07);
  }
  .katex { font-size: 1.18em; }
  /* ── Code as a clean light card ── */
  pre {
    background: #f7faff; border: 1px solid var(--line);
    border-radius: 12px; padding: 14px 18px; box-shadow: 0 2px 12px rgba(15,29,56,.06);
  }
  pre code { background: none; color: #20324f; font-size: 19px; line-height: 1.6; }
  footer {
    left:0; bottom:0; width:100%; box-sizing:border-box; display:flex; padding:0;
    height:26px; font-size:13px; color:#ffffff;
    background: linear-gradient(90deg,#0e1d38 0%,#16294d 30%,#1f3a68 62%,#2a4d86 100%);
  }
  footer span { flex:1; display:flex; align-items:center; justify-content:center;
    border-right:1px solid rgba(255,255,255,.28); }
  footer span:last-child { border-right:none; }
  section::after {
    position:absolute; right:20px; bottom:5px; z-index:10; color:#ffffff;
    font-weight:600; font-size:13px;
    content: attr(data-marpit-pagination) " / " attr(data-marpit-pagination-total);
  }
  /* ── Lead / title ── */
  section.lead { text-align:center; justify-content:center; }
  section.lead::before {
    content:""; position:absolute; top:0; left:0; right:0; height:8px;
    background: linear-gradient(90deg, var(--navy) 0%, var(--accent) 100%);
  }
  .titlebox {
    width:100%; box-sizing:border-box;
    background: linear-gradient(120deg, #16294d 0%, #1F3A68 60%, #2a558f 100%);
    border-radius:16px; padding:30px 44px; margin:10px 0 26px 0;
    box-shadow:0 10px 30px rgba(15,29,56,.22); text-align:center;
  }
  .titlebox h1 { background:none; border:none; color:#fff !important;
    font-size:42px; margin:0; padding:0; letter-spacing:.3px; }
  .titlebox h3 { color:#cfe0ff !important; font-weight:400; border:none;
    margin:10px 0 0 0; display:block; }
  section.lead h1 { color:var(--navy); font-size:42px; }
  section.lead h3 { color:var(--ink); font-weight:400; border:none; display:block; }
  /* ── Components ── */
  .small { font-size:18px; color:var(--muted); }
  .box {
    background:#f7faff; border:1px solid var(--line); border-left:5px solid var(--accent);
    border-radius:0 12px 12px 0; padding:13px 22px; box-shadow:0 2px 12px rgba(15,29,56,.06);
  }
  .warn {
    background:#fff8ec; border:1px solid #f3dca6; border-left:5px solid #e0a51e;
    border-radius:0 12px 12px 0; padding:13px 22px;
  }
  .grid2 { display:grid; grid-template-columns:1fr 1fr; gap:20px; align-items:start; }
  .center { text-align:center; }
  .yes { color:#15803d; font-weight:700; }
  .no  { color:#b04a4a; font-weight:700; }
  /* vertical flow of steps */
  .flow { display:flex; flex-direction:column; align-items:center; gap:5px; margin:14px 0; }
  .flow .step {
    background:#fff; border:1.5px solid #cdd9ec; border-radius:10px;
    padding:9px 22px; font-weight:600; color:var(--navy); font-size:21px;
    box-shadow:0 2px 8px rgba(15,29,56,.06);
  }
  .flow .step.fill { background:var(--navy); color:#fff; border-color:var(--navy); }
  .flow .ar { color:var(--accent); font-size:17px; line-height:1; }
  /* horizontal pill timeline */
  .chips { display:flex; flex-wrap:wrap; align-items:center; gap:7px; justify-content:center; margin:8px 0 4px; }
  .chip { background:var(--navy); color:#fff; border-radius:999px; padding:6px 15px; font-size:18px; font-weight:600; }
  .chip.alt { background:#eef3fb; color:var(--navy); border:1px solid #cdd9ec; }
  .chip.hot { background:linear-gradient(135deg,var(--navy),var(--accent)); }
  .sep { color:#9bb0cf; font-weight:700; }
  /* mono illustration (matrix) */
  .mono {
    background:#0f1f3d; color:#dbe7ff; border-radius:12px; padding:16px 22px;
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    font-size:19px; line-height:1.55; box-shadow:0 4px 16px rgba(15,29,56,.22);
    display:inline-block;
  }
  .mono .dim { color:#7f93bd; }
  .tight table { font-size:18.5px; }
footer: '<span>Nhóm 08 · CS2308</span><span>Hyena Hierarchy (ICML 2023)</span><span>2026</span>'
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
Trần Tú Quang · Tô Huỳnh Minh Tiến · Nguyễn Cao Trung Kiên

<span class="small">Giảng viên hướng dẫn: TS. Nguyễn Văn Kiệt</span>

<!--
Notes:
Mở đầu cả buổi (TV1). Dẫn người nghe từ Transformer/Attention tới đúng "vấn đề" mà Hyena giải quyết. Kết phần này bàn giao cho Tiến (TV2).
-->

---

## Nội dung phần trình bày

1. **Bối cảnh & động lực** — vì sao cần thay thế attention
2. **Nhắc lại nền tảng** — Language Modeling, Perplexity, Transformer
3. **Self-Attention & nút thắt** — cơ chế Q, K, V và chi phí $O(L^2)$
4. **Khoảng cách năng lực & Related Work** — SSM → H3/GSS → Hyena → Mamba

<!--
Notes:
Nói nhanh agenda (~30s): nêu 4 mạch nội dung của phần mình rồi đi vào slide 1.
-->

---

## 1. Câu hỏi nghiên cứu

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
