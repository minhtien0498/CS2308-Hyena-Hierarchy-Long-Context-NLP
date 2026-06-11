# Slide Outline — Đề Tài Hyena Hierarchy
**Môn:** CS2308 – Chuyên đề NLP | **Thời gian:** 15–20 phút | **Số slide:** 12

> Sử dụng file này để làm slide trên Google Slides, PowerPoint, hoặc Canva.
> Mỗi slide có: Tiêu đề · Bullet chính · Hình/Bảng cần có · Speaker note

---

## SLIDE 1 — Trang Bìa
**Tiêu đề:** Khảo Sát và Tái Hiện Kiến Trúc Hyena Hierarchy

**Nội dung:**
- Tên đề tài đầy đủ (in lớn, 2 dòng)
- *Hướng tiếp cận tích chập dưới bậc hai thay thế Attention cho mô hình ngôn ngữ ngữ cảnh dài*
- Tên 3 thành viên nhóm
- Môn: CS2308 – Chuyên đề Nghiên cứu và Ứng dụng về XLNNTNN
- Ngày thuyết trình

**Hình/Bảng:** Logo trường UIT; hình minh họa neural network hoặc sequence model

**Speaker note:**
> "Kính chào thầy/cô và các bạn. Hôm nay nhóm chúng em xin trình bày đề tài về kiến trúc Hyena Hierarchy — một hướng tiếp cận mới nhằm thay thế cơ chế Self-Attention trong Transformer cho các bài toán ngôn ngữ có ngữ cảnh dài. Nhóm gồm 3 thành viên: [tên TV1], [tên TV2], [tên TV3]."

---

## SLIDE 2 — Bối Cảnh và Vấn Đề (Motivation)
**Tiêu đề:** Tại Sao Cần Nghiên Cứu Điều Này?

**Nội dung (3–4 bullet):**
- 🏆 **Transformer** thống trị NLP từ 2017 (BERT, GPT, LLaMA...)
- ⚠️ **Hạn chế cốt lõi:** Self-Attention có độ phức tạp **O(L²)** theo độ dài chuỗi
- 💥 **Thực tế:** Ở L = 64,000 tokens → PyTorch attention **hết RAM (OOM)**
- ❓ **Câu hỏi nghiên cứu:** Có thể thiết kế toán tử **dưới bậc hai** đạt chất lượng tương đương?

**Hình/Bảng:**
- Biểu đồ so sánh complexity: O(L²) vs O(L log L) vs O(L)
- Trục x: Sequence length (256 → 64K), Trục y: Time/Memory
- Annotation: "Transformer OOM ở đây" ở L=8192+

**Speaker note:**
> "Kể từ khi Transformer ra đời năm 2017, hầu hết mọi mô hình ngôn ngữ lớn đều dựa trên cơ chế Self-Attention. Tuy nhiên, Attention có một điểm yếu cơ bản: chi phí tính toán và bộ nhớ tăng theo bậc hai khi sequence length tăng. Điều này đồng nghĩa với việc xử lý văn bản dài — ví dụ như một cuốn sách hay một đoạn code dài — trở nên cực kỳ tốn kém, thậm chí bất khả thi trên GPU thông thường."

---

## SLIDE 3 — Self-Attention Recap
**Tiêu đề:** Self-Attention: Tại Sao O(L²)?

**Nội dung:**
- **Công thức:** `Attention(Q,K,V) = softmax(QKᵀ / √d) · V`
- **Ma trận Attention:** kích thước L × L — mỗi token attend vào mọi token
- **3 đặc tính của Attention:**
  - ✅ Data-controlled (phụ thuộc vào input)
  - ✅ Sublinear parameters (chỉ cần 3 ma trận W_Q, W_K, W_V)
  - ⚠️ Unrestricted context → O(L²) không tránh khỏi

**Hình/Bảng:**
- Sơ đồ ô vuông L×L minh họa attention matrix
- Highlight: khi L tăng 2x → số ô tăng 4x

**Speaker note:**
> "Attention rất mạnh vì mỗi token có thể 'nhìn' vào mọi token khác trong sequence. Nhưng để làm điều đó, cần tính ma trận L×L — và khi L tăng gấp đôi, ma trận tăng gấp bốn. Đây chính là bất lợi quadratic mà Hyena muốn giải quyết."

---

## SLIDE 4 — Landscape: Các Hướng Thay Thế Attention
**Tiêu đề:** Hyena Trong Bối Cảnh Nghiên Cứu

**Nội dung:**
- **Timeline (2020→2023):**
  `Linear Attn (2020) → Performer → S4 (2021) → H3 (2022) → Hyena (2023) → Mamba (2023)`
- **Phân loại kiến trúc:**

| Kiến trúc | Approach | Complexity | Chất lượng |
|---|---|---|---|
| Transformer | Dense Attention | O(L²) | 🟢 Cao |
| S4 / SSM | State Space | O(L log L) | 🟡 Thấp hơn |
| H3 | SSM + Gating | O(L log L) | 🟡 Gần hơn |
| **Hyena** | Conv + Gating | **O(N·L log L)** | **🟢 Match Transformer** |
| Mamba | Selective SSM | O(L) | 🟢 Cao |

**Speaker note:**
> "Nhiều nhóm nghiên cứu đã cố gắng vượt qua hạn chế này. Hyena là một bước đột phá quan trọng năm 2023: lần đầu tiên một kiến trúc attention-free match được Transformer trên benchmark lớn mà không cần hybrid. Và Hyena cũng là tiền thân trực tiếp của Mamba — kiến trúc đang rất được quan tâm hiện nay."

---

## SLIDE 5 — Hyena Hierarchy: Ý Tưởng Chính ⭐
**Tiêu đề:** Hyena = Long Convolution + Gating

**Nội dung:**
- **Recurrence (order N):**
  ```
  z^(n+1) = x^n · FFTConv(h^n, z^n)     n = 1,...,N
  output  = z^(N+1)
  ```
- **2 nguyên thủy đơn giản:**
  - 🔵 `FFTConv(h, v)`: Tích chập dài qua FFT — **O(L log L)** — global memory
  - 🔴 `x^n · (...)`: Nhân element-wise (gating) — **O(L)** — data-controlled
- **Hyena² (N=2) ≈ H3:** 2 bước recurrence, tương đương H3 mechanism
- **Complexity tổng:** O(N · L log₂ L) vs O(L²) của Attention

**Hình/Bảng:** Sơ đồ recurrence (vẽ tay hoặc dùng Figure 1 từ bài báo)

**Speaker note:**
> "Đây là slide trọng tâm nhất. Hyena chỉ cần 2 phép tính cực kỳ đơn giản: tích chập và nhân element-wise. Sức mạnh đến từ việc kết hợp chúng trong nhiều bước. Mỗi tích chập cho phép mô hình 'nhớ' thông tin từ xa — không bị giới hạn bởi cửa sổ local. Còn phép gating cho phép mô hình 'chọn lọc' thông tin dựa trên nội dung thực tế của chuỗi — tương tự vai trò của Q, K trong Attention."

---

## SLIDE 6 — Implicit Long Filter
**Tiêu đề:** Bộ Lọc Ngầm: Tham Số Nhỏ, Độ Nhớ Dài

**Nội dung:**
- **Công thức filter:**
  `h_t = Window(t) · FFN(PositionalEncoding(t))`
- **Tại sao "implicit"?**
  - Explicit (CNN): lưu trực tiếp h ∈ R^L → số tham số = L
  - **Implicit (Hyena):** học hàm γ_θ: t → h_t qua FFN → số tham số = O(1)
- **Ưu điểm:**
  - ✅ Filter length = L (toàn sequence) với ít tham số
  - ✅ Học được decay, high-frequency patterns tự động
  - ✅ Tách biệt memory (L) và parameter count

**Hình/Bảng:** Visualize filter shape: exponential decay + high-frequency (Figure 3 bài báo)

**Speaker note:**
> "Thay vì lưu vector h của L giá trị — sẽ tốn O(L) tham số — Hyena dùng một mạng FFN nhỏ để 'sinh ra' giá trị h_t tại mỗi bước t. Điều này giống như học một công thức thay vì học từng số. Kết quả: filter có thể dài hàng nghìn token nhưng số tham số vẫn nhỏ và cố định."

---

## SLIDE 7 — Tại Sao Hyena Nhanh Hơn?
**Tiêu đề:** Complexity Analysis: O(L log L) vs O(L²)

**Nội dung:**
- **So sánh complexity:**

| Phương pháp | Time | Memory |
|---|---|---|
| Standard Attention | O(L²) | O(L²) |
| FlashAttention | O(L²) tính toán | O(L) |
| **Hyena** | **O(N·L log L)** | **O(L)** |

- **Speedup thực tế (từ bài báo gốc):**
  - **5x** nhanh hơn standard attention ở L=8,192
  - **2x** nhanh hơn FlashAttention ở L=8,192
  - **100x** nhanh hơn FlashAttention ở L=64,000

**Hình/Bảng:** Biểu đồ speedup từ bài báo (Figure về runtime)

**Speaker note:**
> "Cơ chế then chốt là dùng FFT để tính tích chập: thay vì O(L²) phép nhân trực tiếp, FFT chỉ cần O(L log L). Ở sequence length 64,000 — tương đương khoảng 50 trang sách — Hyena nhanh hơn FlashAttention 100 lần và chuẩn Attention thì đã hết RAM từ lâu."

---

## SLIDE 8 — Kết Quả Bài Báo Gốc
**Tiêu đề:** Hyena vs Transformer: Kết Quả Trên Benchmark Lớn

**Nội dung:**
- **WikiText-103:** Hyena đạt **SotA cho attention-free architectures**
- **The Pile (335M params):**
  - Match Transformer perplexity
  - Với **20% ít FLOP hơn**
- **ImageNet (vision):** HyenaViT match standard ViT trong image classification
- **Key message:** Lần đầu tiên attention-free model match Transformer ở scale lớn mà không cần hybridization

**Hình/Bảng:** Bảng kết quả từ bài báo (Table 2 hoặc 3)

**Speaker note:**
> "Bài báo train mô hình 335 triệu tham số trên dataset 825GB — rõ ràng ngoài tầm với sinh viên. Nhưng kết quả rất đáng chú ý: Hyena là kiến trúc đầu tiên hoàn toàn không dùng attention mà vẫn match Transformer ở scale lớn. Điều này mở ra hướng thiết kế mô hình không phụ thuộc vào attention matrix."

---

## SLIDE 9 — Thiết Lập Thực Nghiệm Của Nhóm
**Tiêu đề:** Small-Scale Reproduction: Scope Của Nhóm

**Nội dung:**
- **Phương pháp:** Trend verification (không tái hiện số tuyệt đối)
- **Dataset:** WikiText-2 (~2M tokens, HuggingFace)
- **Mô hình so sánh:**

| | Transformer-small | Hyena-small |
|---|---|---|
| Layers | 4 | 4 |
| d_model | 256 | 256 |
| Heads/Order | 4 heads | N=2 |
| Parameters | ~10M | ~10M |

- **Experiments:** E1 (PPL), E2+E3 (scaling time/memory)
- **Hardware:** Google Colab T4 GPU

**Speaker note:**
> "Nhóm thu nhỏ scope một cách có chủ đích. Mục tiêu không phải là tái hiện số perplexity chính xác như bài gốc, mà là quan sát xu hướng: Hyena có lợi thế gì khi sequence length tăng? Đây là cách tiếp cận hợp lý cho nhóm sinh viên với tài nguyên giới hạn."

---

## SLIDE 10 — Kết Quả Thực Nghiệm
**Tiêu đề:** Kết Quả: Transformer vs Hyena

**Nội dung:**
- **E1 — Baseline (L=256):**
  - [Bảng PPL Transformer vs Hyena sau N epoch]
  - Nhận xét: tương đương ở scale nhỏ
- **E2+E3 — Scaling:**
  - [Bảng Time/Memory theo L: 256 → 512 → 1024]
  - Khi L tăng 2x: Transformer time tăng ~4x, Hyena tăng ~2x

**Hình/Bảng:**
- Loss curves (train/val theo epoch) — TV3 điền sau khi train
- Bảng time/memory scaling — TV3 điền sau khi chạy E2/E3
- [Placeholder: điền kết quả thực tế sau khi chạy]

**Speaker note:**
> "Kết quả E1 cho thấy ở scale nhỏ, perplexity của hai mô hình khá gần nhau — điều này nhất quán với kết quả bài gốc: Hyena cần scale lớn để thể hiện rõ lợi thế về chất lượng ngôn ngữ. Tuy nhiên, ở E2 và E3, xu hướng scaling rõ ràng hơn: Hyena scale tốt hơn đáng kể về thời gian và bộ nhớ khi L tăng."

---

## SLIDE 11 — Thảo Luận và Kết Luận
**Tiêu đề:** Nhận Xét: Ưu và Nhược Điểm Của Hyena

**Nội dung:**

| | Ưu điểm | Nhược điểm |
|---|---|---|
| **Complexity** | O(L log L) thực sự subquadratic | Cần scale lớn để thấy lợi thế PPL |
| **Memory** | Không lưu attention matrix L×L | FFT overhead ở sequence ngắn |
| **Context** | Unbounded context (toàn sequence) | Implicit filter khó giải thích hơn |
| **Code** | Pure PyTorch, không cần CUDA custom | Phức tạp hơn Transformer đơn thuần |

- **Kết luận:** Hyena là bước đột phá quan trọng; Mamba (2023) đơn giản hóa thêm
- **Hướng tương lai:** Mamba, Mamba-2, RetNet, RWKV

**Speaker note:**
> "Nhóm kết luận: Hyena đã chứng minh rằng attention không phải là cần thiết duy nhất để đạt chất lượng ngôn ngữ cao. Tuy nhiên, ở quy mô nhỏ — như thực nghiệm của nhóm — sự khác biệt về perplexity chưa rõ ràng. Điểm mạnh rõ ràng nhất là khả năng scaling với sequence length dài. Đây mở đường cho các kiến trúc sau như Mamba đơn giản hóa hơn nữa."

---

## SLIDE 12 — Q&A và Tài Liệu Tham Khảo
**Tiêu đề:** Cảm Ơn — Q&A

**Nội dung:**
- **GitHub:** [Link repo nhóm]
- **Tài liệu tham khảo chính:**
  1. Poli et al. (2023). *Hyena Hierarchy*. ICML 2023.
  2. Vaswani et al. (2017). *Attention Is All You Need*. NeurIPS.
  3. Gu et al. (2021). *S4*. ICLR 2022.
  4. Dao et al. (2022). *H3*. ICLR 2023.
  5. Dao et al. (2022). *FlashAttention*. NeurIPS.
  6. Merity et al. (2016). *WikiText*. ICLR.

**Hình/Bảng:** QR code link GitHub repo (tạo tại qr-code-generator.com)

**Speaker note:**
> "Xin cảm ơn thầy/cô và các bạn đã lắng nghe. Nhóm sẵn sàng trả lời câu hỏi. Toàn bộ code và kết quả thực nghiệm có thể truy cập tại GitHub repo của nhóm."

---

## Hướng Dẫn Làm Slide

### Công cụ đề xuất
- **Google Slides:** Cộng tác dễ, share link trực tiếp
- **Canva:** Template đẹp, nhiều hình minh họa sẵn
- **PowerPoint:** Quen thuộc, xuất PDF dễ

### Palette màu đề xuất
- **Primary:** `#1E3A5F` (navy blue)
- **Accent:** `#E74C3C` (red — dùng cho Hyena)
- **Accent 2:** `#2980B9` (blue — dùng cho Transformer)
- **Background:** `#F8F9FA` (light gray)
- **Text:** `#2C3E50` (dark)

### Font đề xuất
- **Title:** Inter Bold hoặc Roboto Bold
- **Body:** Inter Regular, size 18–20
- **Code:** JetBrains Mono hoặc Consolas

### Template layout đề xuất
- Header: Màu primary `#1E3A5F`, chữ trắng
- Body: Nền trắng/light gray
- Footer: Tên nhóm + slide number
- Highlight keyword: In đậm + màu accent
