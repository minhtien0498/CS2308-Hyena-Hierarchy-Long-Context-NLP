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

1. **Bối cảnh và động lực**: tại sao cần nghiên cứu
2. **Định nghĩa bài toán**: ba thuộc tính của attention và định nghĩa Hyena
3. **Đào sâu toán học**: recurrence, ma trận data-controlled, FFTConv, độ phức tạp
4. **Dữ liệu và đánh giá**: synthetic benchmark và benchmark chuẩn
5. **Kết quả và ảnh hưởng**
6. **Thực nghiệm**: Transformer-small và Hyena-small trên WikiText-2

---

## 1. Bối cảnh & Động lực

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

## Khoảng cách năng lực (capability gap)

Vì sao các toán tử rẻ trước đây thua attention? Nhóm tác giả dùng **mechanistic interpretability** để truy ra 3 năng lực mấu chốt mà chúng thiếu:

| Năng lực | SSM / Conv cố định | Attention |
|---|---|---|
| Phụ thuộc dữ liệu (data control) | Không, tĩnh | Có, `A(u)` |
| Ngữ cảnh không giới hạn | Không, thường bị locality | Có |
| Số tham số độc lập độ dài chuỗi | Có | Có |

Hyena được thiết kế để **giữ đồng thời cả ba**: thay vì xấp xỉ attention, nhóm tác giả tái dựng các tính chất của nó bằng primitive rẻ hơn.

---

## 2. Định nghĩa bài toán

### Ba thuộc tính cần bảo toàn

Phân rã self-attention: $y = A(q,k)\,v$, với $A(u)=\mathrm{SoftMax}\!\big(\tfrac{1}{\sqrt D}\,uM_q M_k^\top u^\top\big)$.

1. **Data control**: `A(u)` là toán tử tuyến tính *do dữ liệu quyết định*, một khối mã hóa cả họ hàm tuyến tính.
2. **Sublinear parameter scaling**: số tham số **tách rời** độ dài chuỗi, nhờ vậy dồn được tham số vào FFN.
3. **Unrestricted context**: không áp đặt locality, cho phép phụ thuộc tầm xa giữa bất kỳ hai vị trí.

<div class="box">

**Ý tưởng Hyena:** thay vì xấp xỉ ma trận attention, hãy xây một toán tử **data-controlled** mới từ hai primitive rẻ: **long convolution** + **element-wise gating**.

</div>

---

## Định nghĩa toán tử Hyena (bậc N)

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

## 3. Đào sâu toán học

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

## Vì sao Hyena tổng quát hóa H3 & GSS

H3 (Dao et al.) thực ra là một phân rã 3 thừa số:

$$
A(q,k) = D_q\, S_\psi\, D_k\, S_\varphi, \qquad H3(q,k,v)=A(q,k)v
$$

- **Hyena bậc 2** tương đương cơ chế **H3**.
- **Hyena bậc 1** tương đương **GSS**, với một cách tham số hóa cụ thể cho bộ lọc (qua SSM).
- Hyena tổng quát hóa lên **bậc N tùy ý** và bộ lọc **dạng tự do (free-form)** thay vì buộc qua SSM.

Đây chính là ý nghĩa "hierarchy": một họ toán tử có thứ bậc, các mô hình trước là tầng thấp.

---

## FFTConv: tính convolution dài mà không vật chất hóa ma trận

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

## Độ phức tạp & đối ngẫu miền thời gian/tần số

**Độ phức tạp toàn toán tử bậc N** (Proposition 3.2):

$$
\mathcal{O}\big(N\,D\,L\,(\log_2 L + D)\big) \;\ll\; \mathcal{O}(L^2)
$$

**Trực giác: đối ngẫu hai miền**
- *Convolution ở miền thời gian* tương đương *nhân element-wise ở miền tần số* (và ngược lại).
- Hyena **luân phiên** giữa convolution (mở rộng "memory", gom ngữ cảnh rộng) và gating (nhân element-wise để lựa chọn thành phần tần số tinh tế).

Sự đan xen này là một giả thuyết lý giải vì sao Hyena hiệu quả: vừa nhìn xa, vừa lọc chọn lọc.

---

## Bộ lọc ngầm & tính nhân quả

Bộ lọc dài **không** học như một vector tham số khổng lồ, mà **sinh ra từ một FFN nhỏ** (implicit parametrization):

$$
h_t = \mathrm{Window}(t)\cdot\big(\mathrm{FFN}\circ \mathrm{PositionalEncoding}\big)(t)
$$

- **Tách rời** độ dài bộ lọc khỏi số tham số (sublinear scaling).
- `Window(t)=exp(-αt)` cho suy giảm mũ, điều hòa độ dài hiệu dụng; sine tần số cao trong FFN chống *low-frequency bias*.

**Proposition 3.1 (Causal Hyenas):** nếu mọi $h^n$ nhân quả thì toán tử Hyena nhân quả, nhờ vậy huấn luyện tự hồi quy được (như mask tam giác của Transformer).

---

## 4. Dữ liệu & Đánh giá

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

## Các phương pháp đánh giá

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

## 5. Kết quả & Ảnh hưởng

### Tác động của nghiên cứu

- **Thách thức "attention is all you need":** kiến trúc dưới bậc hai, đơn giản hơn, *có thể* sánh ngang Transformer ở quy mô dưới 1 tỷ tham số, dẫn tới nhận định *“attention may not be all we need.”*
- **Mở đường ngữ cảnh siêu dài:** Hyena là nền cho **HyenaDNA, Evo** (bộ gene, chuỗi 10⁵ đến 10⁶ token) và **StripedHyena**, cộng hưởng với dòng **SSM, Mamba** ở những nơi attention bất khả thi.
- **Diễn giải cơ chế thành công cụ thiết kế:** benchmark recall và induction trở thành la bàn thiết kế kiến trúc, không chỉ để chấm điểm.
- **Primitive tổng quát:** dùng được ngoài ngôn ngữ, cho cả ảnh, âm thanh, sinh học.

> Thông điệp kết: hiểu *vì sao* attention mạnh quan trọng hơn việc *sao chép* attention.

---

## 6. Thực nghiệm

### Phạm vi & mục tiêu

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

<span class="small">Kết quả sơ bộ sau 5 epoch, chạy bằng notebook <code>notebooks/colab_E1_run.ipynb</code>. Loss vẫn đang giảm nên đây là số minh hoạ xu hướng, chưa phải mức hội tụ cuối.</span>

Nhận xét: hai model cùng cỡ tham số cho perplexity cùng tầm, Hyena còn nhỉnh hơn một chút. Đủ để nói Hyena là một baseline ngôn ngữ hợp lệ ở quy mô này.

---

## Kết quả: tốc độ theo độ dài chuỗi

Đo thời gian forward với input giả, cùng cấu hình model 16M tham số, batch 8, trên Colab T4. Tăng dần độ dài L:

| L | Transformer (ms) | Hyena (ms) | Tỉ lệ |
|---|---|---|---|
| 256 | 21.4 | 21.9 | Hyena chậm hơn chút |
| 512 | 43.7 | 42.4 | hai bên hòa nhau |
| 1024 | 100.1 | 84.1 | Hyena nhanh hơn ~1.19 lần |

Ở L=2048 Hyena vẫn chạy tốt (khoảng 168 ms) trong khi Transformer bắt đầu đuối. Attention tăng theo bình phương độ dài, còn Hyena tăng gần tuyến tính, nên chuỗi càng dài Hyena càng lợi.

---

## Thảo luận và giới hạn

- Ở chuỗi ngắn Hyena chậm hơn, vì chi phí FFT và đệm 2L lớn hơn phần tiết kiệm được. Hyena hòa ở khoảng L bằng 512 và vượt lên từ L bằng 1024, đúng như lưu ý trong paper.
- Bản cài của nhóm có đơn giản hóa so với safari: filter dùng SiLU thay cho activation dạng sin, modulation rút gọn, bỏ skip-connection. Vì vậy hội tụ có thể chậm hơn bản gốc.
- Vì dùng thuần PyTorch và không có CUDA kernel, nhóm chưa đạt mức speedup tuyệt đối như paper.
- Phần đo tốc độ dùng input giả để đo thời gian forward, không phải đánh giá perplexity trên tập validation.
- Cần phân biệt rõ: số trên WikiText-103, The Pile và speedup từ 8K đến 64K là của paper gốc, còn số WikiText-2 ở đây là của nhóm.

---

## Kết luận phần tái hiện

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
