# TV2 - Block Q&A Cho File Q&A Chung

> Phục vụ yêu cầu [phan_cong_present_hyena_3_tuan.md §6](../../phan_cong_present_hyena_3_tuan.md):
> *"File Q&A chung: Cả nhóm cùng cập nhật. Bước 2: TV2 điền phần Q&A Hyena method và paper results vào file chung."*

Cách dùng: copy block dưới đây vào file Q&A chung của nhóm (chưa tồn tại — cả nhóm chốt format), dán vào mục **TV2 — Hyena method & paper results**. Đây là bản đã chắt từ [qna_tv2.md](qna_tv2.md), giữ các câu sát nhất với phần TV2 trình bày, không trùng TV1/TV3.

Người trả lời chính: **TV2 (Tiến)**. Người bổ sung: **TV1**.

---

## TV2 — Hyena Method

### Q: Hyena có phải là xấp xỉ (approximation) attention không?
Không. Hyena không xấp xỉ trực tiếp attention matrix. Nó xây một operator mới từ long convolution và gating, nhằm giữ các tính chất quan trọng của attention (data control, context dài, số tham số không phụ thuộc tuyến tính vào L) nhưng rẻ hơn.

### Q: Vì sao chỉ convolution là chưa đủ?
Convolution thường dùng filter khá tĩnh, không đổi theo nội dung input. Language modeling cần chọn lọc theo ngữ cảnh. Hyena thêm gate `xⁿ` chiếu từ input, nhân element-wise với output convolution → output phụ thuộc dữ liệu.

### Q: Công thức recurrence Hyena nói gì?
`z^(n+1)_t = xⁿ_t · (hⁿ * zⁿ)_t`. Ở bước n: lấy trạng thái `zⁿ`, chập với long filter `hⁿ`, rồi nhân với gate `xⁿ`. Lặp N lần ra output. Convolution mang thông tin xa, gate điều khiển theo dữ liệu.

### Q: Implicit filter là gì, vì sao giảm tham số?
Thay vì học trực tiếp vector filter dài L (tham số tăng theo L), Hyena học hàm `h_t = Window(t)·FFN(PositionalEncoding(t))`. Số tham số nằm trong FFN, ~O(1) theo L → filter dài tùy ý mà tham số không nổ.

### Q: Vì sao FFTConv đạt O(L log L)?
Theo convolution theorem: convolution trong miền thời gian = nhân element-wise trong miền tần số. Lấy FFT(h), FFT(u), nhân, rồi iFFT. Chi phí FFT là O(L log L). Trong repo: [models/hyena.py `_causal_fft_conv`](../../../models/hyena.py#L194).

### Q: "Causal" trong Hyena đạt bằng cách nào, mà không cần mask như Transformer?
Zero-pad 2L rồi lấy L phần tử đầu ([hyena.py:212](../../../models/hyena.py#L212)) → convolution tuyến tính (aperiodic) → token tại t chỉ thấy t' ≤ t. Tương đương Proposition 3.1 (Causal Hyenas) trong paper: nếu mọi filter hⁿ causal thì toàn operator causal.

### Q: Order-N hierarchy nghĩa là gì? Liên hệ H3/GSS?
N là số bước lặp convolution + gating. N lớn → operator phong phú hơn. Paper chỉ ra H3 ≈ Hyena₂, GSS ≈ Hyena₁; Hyena tổng quát lên bậc N + filter free-form. Nhóm dùng order=2.

---

## TV2 — Kết Quả Paper Gốc

### Q: Paper chứng minh Hyena "tốt hơn" Transformer không?
Không nói chung chung. Paper cho thấy Hyena **match** Transformer trong một số setting (WikiText-103, The Pile 335M) và **nhanh hơn rõ** ở long-context. Transformer vẫn rất mạnh, được tối ưu tốt.

### Q: Bài báo này có gì mới, và vì sao đáng được đăng?
Điểm mới quan trọng là Hyena không chỉ tối ưu attention hiện có, mà đề xuất một **operator attention-free mới** cho language modeling. Operator này kết hợp long convolution, data-controlled gating và implicit filter để vừa giữ phụ thuộc xa, vừa có độ phức tạp subquadratic khoảng `O(N · L log L)`.

So với Transformer, Hyena tránh bottleneck ma trận attention `L x L` khi context dài. So với các hướng attention-free trước như S4/H3/GSS, Hyena tổng quát hóa tốt hơn, filter linh hoạt hơn, và thu hẹp quality gap với Transformer mà không cần hybrid với attention.

Nếu trả lời ngắn trước lớp: đây là bài có **novelty về kiến trúc**, **lý do lý thuyết rõ**, và **thực nghiệm đủ mạnh** nên đáng chú ý ở thời điểm ICML 2023.

### Q: Số liệu nổi bật nhất của paper?
- WikiText-103: Hyena-3 PPL ~18.6, ngang Transformer 125M.
- The Pile 335M: Hyena-2 gần Transformer, giảm ~20% **non-parametric** FLOPs.
- Long-context: ~2× vs FlashAttention @ L=8K; ~100× @ L=64K; crossover vs attention @ L≈2048, vs FlashAttention @ L≈4096–8192.
- Associative recall tới **131k token** — lần đầu attention-free làm ICL ở độ dài này.

### Q: Kết quả paper gốc có phải kết quả nhóm không?
Không. TV2 chỉ trình bày kết quả Poli et al. Kết quả reproduction nhóm (WikiText-2, ~16M params) nằm ở phần TV3, mục tiêu là kiểm chứng xu hướng, không claim match số tuyệt đối.

### Q: Hạn chế của Hyena là gì?
Cần kernel FFTConv tối ưu để đạt lý thuyết; pure PyTorch có overhead ở sequence ngắn; hội tụ nhạy hyperparameter ở scale nhỏ. → Đây cũng là lý do kết quả nhóm có thể chưa thấy rõ lợi thế PPL.

### Q: Vì sao có thể Hyena chậm hơn ở kết quả reproduction?
Sequence length chưa đủ lớn, pure PyTorch FFT chưa tối ưu, overhead FFT lớn ở ~16M params. Lợi thế runtime rõ nhất ở `L` lớn + kernel tối ưu. Xem [experiment/scaling_analysis.md](../experiment/scaling_analysis.md).
