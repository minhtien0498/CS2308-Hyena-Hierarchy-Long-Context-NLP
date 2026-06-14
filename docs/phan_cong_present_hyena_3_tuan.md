# Phân Công Công Việc Present Bài Báo Hyena Hierarchy

**Môn:** CS2308 - Chuyên đề Nghiên cứu và Ứng dụng về Xử lý Ngôn ngữ Tự nhiên  
**Bài báo:** *Hyena Hierarchy: Towards Larger Convolutional Language Models* - Poli et al., ICML 2023  
**Thời gian còn lại:** khoảng 3 tuần  
**Số thành viên:** 3  
**Thời lượng trên lớp:** 45 phút trình bày + 15 phút hỏi đáp  
**Định hướng:** trình bày lại bài báo, có liên hệ với phần tái hiện quy mô nhỏ của nhóm

---

## 1. Mục Tiêu Buổi Trình Bày

Nhóm cần làm rõ 4 ý chính:

1. Bài báo giải quyết vấn đề gì trong NLP hiện đại.
2. Vì sao Self-Attention trong Transformer gặp bottleneck khi chuỗi dài.
3. Hyena Hierarchy thay thế Attention bằng cơ chế nào.
4. Nhóm tái hiện bài báo ở quy mô nhỏ như thế nào, kết quả và giới hạn là gì.

Thông điệp chính cần thống nhất:

> Transformer rất mạnh, nhưng Self-Attention có chi phí `O(L^2)` theo độ dài chuỗi. Hyena đề xuất một toán tử không dùng attention, kết hợp **long convolution qua FFT** và **data-controlled gating**, đạt độ phức tạp dưới bậc hai `O(N * L log L)`. Trong phạm vi môn học, nhóm không tái hiện toàn bộ mô hình lớn của bài báo mà thực hiện small-scale reproduction để kiểm chứng xu hướng.

---

## 2. Cấu Trúc Trình Bày 45 Phút

Với yêu cầu **45 phút phần nói**, nên tăng từ 24 slide lên khoảng **33 slide**. Mỗi thành viên phụ trách **11 slide**, tương ứng khoảng **15 phút/người**. Trung bình mỗi slide nói khoảng **75-90 giây**; các slide công thức hoặc kết quả có thể nói lâu hơn, các slide chuyển ý nên nói nhanh.

| Thành viên | Vai trò chính | Slide | Thời lượng |
|---|---|---:|---:|
| TV1 | Nền tảng, motivation, Self-Attention, related work | 1-11 | 15 phút |
| TV2 | Phương pháp Hyena và kết quả bài báo gốc | 12-22 | 15 phút |
| TV3 | Reproduction của nhóm, kết quả, thảo luận, kết luận và chuyển sang Q&A | 23-33 | 15 phút |

Tổng: 33 slide, 45 phút.

Không nên tăng lên quá 36 slide vì bài có nhiều công thức và phần hỏi đáp dài. 33 slide là mức cân bằng: đủ tách ý, nhưng vẫn có thời gian giải thích.

---

## 3. Mạch Nội Dung Chung

Bài trình bày phải đi theo một mạch thống nhất:

```text
Transformer mạnh
-> Self-Attention bị O(L^2) khi chuỗi dài
-> Các hướng thay thế attention trước Hyena vẫn còn capability gap
-> Hyena giữ lại các tính chất quan trọng của attention bằng long convolution + gating
-> Bài báo chứng minh Hyena match Transformer ở một số benchmark lớn và nhanh hơn ở long-context
-> Nhóm tái hiện ở quy mô nhỏ để kiểm chứng xu hướng
```

Mỗi thành viên không trình bày như một phần độc lập. Phần của người trước phải tạo đầu vào cho người sau.

---

## 4. Kiến Thức Nền Cần Học

| Chủ đề | Mức cần nắm | Người học chính | Người còn lại cần hiểu để nối ý |
|---|---|---|---|
| Language Modeling | Autoregressive LM, next-token prediction, perplexity | TV3 | TV1, TV2 |
| Transformer | Embedding, positional encoding, attention, FFN, residual | TV1 | TV2, TV3 |
| Self-Attention | Q,K,V, attention matrix `L x L`, causal mask | TV1 | TV2, TV3 |
| Complexity | Vì sao Attention tốn `O(L^2)` time/memory | TV1 | TV2 |
| Long Convolution | Convolution trên toàn chuỗi, khác CNN kernel ngắn | TV2 | TV1, TV3 |
| FFTConv | Dùng FFT để tính convolution với chi phí `O(L log L)` | TV2 | TV1, TV3 |
| Gating | Gate phụ thuộc input giúp Hyena có tính data-controlled | TV2 | TV1 |
| SSM, H3, GSS, Mamba | Biết vị trí của Hyena trong dòng nghiên cứu thay thế attention | TV1 + TV2 | TV3 |
| Reproduction | WikiText-2, tokenizer, Transformer-small, Hyena-small, PPL/runtime | TV3 | TV1, TV2 |

---

## 5. Liên Kết Đầu Ra Giữa Các Thành Viên

| Đầu ra của ai | Bàn giao cho ai | Dùng để làm gì |
|---|---|---|
| TV1: giải thích `O(L^2)` của Attention | TV2 | TV2 so sánh với `O(N * L log L)` của Hyena |
| TV1: 3 tính chất của Attention cần giữ lại | TV2 | TV2 giải thích vì sao Hyena cần convolution + gating |
| TV1: related work SSM/H3/GSS | TV2 | TV2 nói Hyena tổng quát hóa H3/GSS như thế nào |
| TV2: công thức Hyena recurrence | TV3 | TV3 liên hệ với implementation `models/hyena.py` |
| TV2: kết quả và speedup trong paper | TV3 | TV3 so sánh với kết quả reproduction của nhóm |
| TV3: setup reproduction | TV1, TV2 | Cả nhóm hiểu rõ scope, tránh nói quá mức kết quả nhóm |
| TV3: bảng/plot kết quả | Cả nhóm | Dùng ở slide kết quả và phần hỏi đáp |

Câu chuyển tiếp nên dùng:

- TV1 -> TV2: "Sau khi thấy Attention mạnh nhưng bị giới hạn bởi `O(L^2)`, câu hỏi là có thể giữ các tính chất tốt của Attention bằng một toán tử rẻ hơn không. Đó là ý tưởng dẫn đến Hyena."
- TV2 -> TV3: "Bài báo kiểm chứng Hyena ở quy mô lớn. Trong phạm vi môn học, nhóm thu nhỏ bài toán để tái hiện xu hướng trên WikiText-2."
- TV3 -> Q&A: "Kết quả của nhóm là small-scale reproduction; các kết luận về scale lớn dựa trên bài báo gốc. Sau đây nhóm xin chuyển sang phần hỏi đáp, mỗi thành viên sẽ trả lời theo phần mình phụ trách."

---

## 6. Phân Công Chuẩn Bị Hỏi Đáp

Phần hỏi đáp 15 phút **chia theo phần trình bày của từng thành viên**. Không để TV3 hoặc bất kỳ một người nào ôm toàn bộ Q&A. Mỗi thành viên chịu trách nhiệm chuẩn bị, luyện trả lời và cập nhật câu hỏi cho phần mình.

**Nguyên tắc chia việc:** ai trình bày phần nào thì chuẩn bị câu hỏi phần đó; câu hỏi giao giữa nhiều phần thì người liên quan cùng bổ sung.

| Nhóm câu hỏi | Người chuẩn bị chính | Người hỗ trợ | Nội dung cần chuẩn bị |
|---|---|---|---|
| Transformer, Self-Attention, `O(L^2)` | TV1 | TV2 | Vì sao attention tốn bộ nhớ, FlashAttention khác gì, long-context quan trọng thế nào |
| Related work | TV1 | TV2 | SSM, S4, H3, GSS, Mamba, Hyena nằm ở đâu trong dòng nghiên cứu |
| Hyena operator | TV2 | TV1 | Long convolution, gating, recurrence, implicit filter, FFTConv |
| Kết quả bài báo gốc | TV2 | TV1 | WikiText-103, The Pile, synthetic tasks, speedup 8K/64K |
| Reproduction của nhóm | TV3 | TV2 | Dataset, model config, PPL, runtime/memory, vì sao chỉ làm small-scale |
| Câu hỏi phản biện/giới hạn | Cả nhóm | Người gần phần câu hỏi nhất trả lời trước | Vì sao kết quả nhóm có thể khác paper, hạn chế tài nguyên, hạn chế implementation |

Output cuối cùng của phần Q&A:

| Output | Người chịu trách nhiệm | Yêu cầu |
|---|---|---|
| Q&A phần lý thuyết | TV1 | Ít nhất 5 câu về Transformer, Attention, complexity, related work |
| Q&A phần Hyena method | TV2 | Ít nhất 5 câu về recurrence, convolution, gating, FFTConv, paper results |
| Q&A phần reproduction | TV3 | Ít nhất 5 câu về dataset, code, setup, kết quả, giới hạn |
| File Q&A chung | Cả nhóm cùng cập nhật | Ghép 15-20 câu vào một file chung, chia theo 3 mục TV1/TV2/TV3 |
| Bảng phân công trả lời | Cả nhóm thống nhất | Mỗi nhóm câu hỏi ghi rõ người trả lời trước và người bổ sung |

Nguyên tắc khi trả lời:

1. Câu hỏi thuộc phần ai thì người đó trả lời trước.
2. Nếu câu hỏi giao giữa hai phần, người phụ trách phần gần nhất trả lời trước, người còn lại bổ sung.
3. Nếu câu hỏi quá rộng, TV1 trả lời phần motivation/nền tảng, TV2 trả lời phần method/paper, TV3 trả lời phần reproduction.
4. Không nói quá kết quả reproduction; luôn tách riêng kết quả bài báo gốc và kết quả nhóm.

Để tránh lệch tải, file Q&A chung nên được làm theo cách:

| Bước | Người làm | Output |
|---|---|---|
| 1 | TV1 | Điền phần Q&A lý thuyết vào file chung |
| 2 | TV2 | Điền phần Q&A Hyena method và paper results vào file chung |
| 3 | TV3 | Điền phần Q&A reproduction vào file chung |
| 4 | Cả nhóm | Review chéo, bổ sung câu hỏi khó và thống nhất người trả lời |

---

## 7. Phân Công Slide Chi Tiết

### TV1 - Nền Tảng, Motivation, Related Work

**Vai trò:** giúp người nghe hiểu vì sao bài báo cần thiết.

| Slide | Tiêu đề | Nội dung chính | Output cần chuẩn bị |
|---:|---|---|---|
| 1 | Trang bìa | Tên bài, tác giả, ICML 2023, nhóm | Slide mở đầu |
| 2 | Câu Hỏi Nghiên Cứu | "Is attention all we need?" và mục tiêu của paper | 1 câu research question |
| 3 | Vì Sao Long-Context Quan Trọng | Tài liệu dài, code dài, hội thoại dài, sinh học | Ví dụ ứng dụng |
| 4 | Language Modeling | Next-token prediction, perplexity | Công thức PPL đơn giản |
| 5 | Transformer Recap | Transformer block và vai trò của Attention | Sơ đồ block |
| 6 | Self-Attention Mechanics | Q,K,V, `softmax(QK^T/sqrt(d))V` | Công thức |
| 7 | Attention Matrix | Ma trận `L x L`, causal mask, mỗi token nhìn các token trước | Hình ma trận attention |
| 8 | Bottleneck `O(L^2)` | Time/memory tăng bậc hai khi L tăng | Bảng ví dụ L tăng 2x -> chi phí 4x |
| 9 | FlashAttention và Giới Hạn | FlashAttention tối ưu memory access nhưng compute vẫn `O(L^2)` | So sánh ngắn |
| 10 | Capability Gap | 3 tính chất cần giữ: data control, sublinear parameters, unrestricted context | Bảng 3 tính chất |
| 11 | Related Work | SSM, S4, H3, GSS, Mamba, vị trí của Hyena | Timeline/bảng so sánh |

**Output bắt buộc của TV1:**

| Output | Mô tả |
|---|---|
| Note Self-Attention | Giải thích Q,K,V, attention matrix, causal mask, `O(L^2)` |
| Bảng related work | So sánh Transformer, SSM/S4, H3, Hyena, Mamba |
| Speaker notes | Lời nói cho slide 1-11, khoảng 15 phút |
| Q&A lý thuyết | Ít nhất 5 câu hỏi và câu trả lời về Attention/Transformer/related work |

---

### TV2 - Phương Pháp Hyena và Kết Quả Bài Báo Gốc

**Vai trò:** trình bày phần cốt lõi của paper: Hyena hoạt động như thế nào và paper chứng minh điều gì.

| Slide | Tiêu đề | Nội dung chính | Output cần chuẩn bị |
|---:|---|---|---|
| 12 | Từ Attention Sang Hyena | Nhắc lại vấn đề: cần operator rẻ hơn nhưng vẫn data-controlled | Slide chuyển ý |
| 13 | Ý Tưởng Chính | Hyena = long convolution + gating | Sơ đồ ý tưởng |
| 14 | Long Convolution | Filter dài bằng toàn sequence, khác CNN local | Hình minh họa filter dài |
| 15 | Data-Controlled Gating | Gate phụ thuộc input, giúp chọn lọc thông tin | Ví dụ trực quan |
| 16 | Hyena Recurrence | `z^(n+1)_t = x^n_t * (h^n * z^n)_t` | Công thức + giải thích từng thành phần |
| 17 | Order-N Hierarchy | Ý nghĩa bậc N, Hyena bậc thấp liên hệ H3/GSS | Sơ đồ recurrence nhiều tầng |
| 18 | Matrix View | Diagonal gating + Toeplitz convolution | Hình matrix decomposition |
| 19 | Implicit Filter | FFN sinh filter theo vị trí, không học trực tiếp vector dài L | Công thức `h_t = Window(t) * FFN(PE(t))` |
| 20 | FFTConv | FFT -> nhân element-wise -> iFFT | Sơ đồ FFTConv |
| 21 | Complexity và Ý Nghĩa | Hyena `O(N * L log L)` so với Attention `O(L^2)` | Bảng complexity |
| 22 | Kết Quả Paper Gốc | Synthetic tasks, WikiText-103, The Pile, speedup 8K/64K | Bảng kết quả + speedup |

**Output bắt buộc của TV2:**

| Output | Mô tả |
|---|---|
| Note Hyena operator | Recurrence, long convolution, gating, implicit filter, FFTConv |
| Sơ đồ Hyena | Một hình thể hiện projection -> gating -> FFTConv -> output |
| Bảng kết quả paper | Synthetic, WikiText-103, The Pile, speedup |
| Speaker notes | Lời nói cho slide 12-22, khoảng 15 phút |
| Q&A method | Ít nhất 5 câu hỏi và câu trả lời về Hyena/FFT/gating/filter |

---

### TV3 - Reproduction, Kết Quả Nhóm, Thảo Luận

**Vai trò:** cho thấy nhóm hiểu bài báo và đã tái hiện ở quy mô phù hợp với tài nguyên môn học.

| Slide | Tiêu đề | Nội dung chính | Output cần chuẩn bị |
|---:|---|---|---|
| 23 | Scope Của Nhóm | Không tái hiện full paper, chỉ small-scale reproduction | Lý do thu nhỏ scope |
| 24 | Mục Tiêu Reproduction | Trend verification: PPL và scaling theo sequence length | Câu hỏi thực nghiệm |
| 25 | Dataset | WikiText-2, tokenizer, sequence length | Bảng dataset/pipeline |
| 26 | Pipeline | Load data -> tokenize -> dataloader -> train -> evaluate | Sơ đồ pipeline |
| 27 | Transformer-Small | Baseline GPT-like, layers/heads/d_model | Bảng cấu hình Transformer |
| 28 | Hyena-Small | Mapping từ Hyena paper sang implementation nhỏ | Bảng cấu hình Hyena |
| 29 | Training/Evaluation | Loss, perplexity, runtime/memory, hardware | Quy trình train/evaluate |
| 30 | Kết Quả E1 | PPL/loss Transformer vs Hyena | Bảng kết quả E1 |
| 31 | Kết Quả Scaling | Runtime/memory theo sequence length nếu có | Runtime/memory plot |
| 32 | Thảo Luận và Giới Hạn | Scale nhỏ, epoch ít, pure PyTorch FFT, hardware | 3-5 bullet trung thực |
| 33 | Kết Luận & Q&A | Takeaways, references, GitHub/repo, chuyển sang hỏi đáp | Slide kết thúc |

**Output bắt buộc của TV3:**

| Output | Mô tả |
|---|---|
| Bảng setup reproduction | Dataset, tokenizer, model config, hardware, metric |
| Bảng kết quả nhóm | PPL/loss, runtime/memory nếu có |
| Plot kết quả | Loss curve hoặc runtime plot |
| Nhận xét giới hạn | Nói rõ scale nhỏ, epoch ít, pure PyTorch FFT, hardware |
| Q&A reproduction | Ít nhất 5 câu hỏi và câu trả lời về code/dataset/kết quả |

---

## 8. Phần Thực Nghiệm Cần Chốt

Hiện repo đã có code cho training/evaluation và một plot runtime ở `results/plots/reproduce_runtime.png`, nhưng **chưa thấy CSV kết quả E1/E2/E3 trong thư mục `results/`**. Vì vậy phần thực nghiệm vẫn cần chốt số liệu trước khi làm slide cuối.

Phần thực nghiệm không nên dồn hết cho TV3. Cách chia hợp lý là:

- **TV1** phụ trách tiêu chí đánh giá và diễn giải kết quả theo paper.
- **TV2** phụ trách kiểm tra mô hình, complexity và phần scaling runtime/memory.
- **TV3** phụ trách chạy pipeline, gom số liệu, tạo bảng/plot cuối.

### 8.1 Mức Tối Thiểu Phải Có

| Mức | Output | Dùng cho slide |
|---|---|---|
| Bắt buộc | Bảng dataset/model/hardware/metric | Slide 25-29 |
| Bắt buộc | E1: bảng Transformer-small vs Hyena-small tại `seq_len=256` | Slide 30 |
| Bắt buộc | E2/E3: bảng runtime scaling theo sequence length | Slide 31 |
| Bắt buộc | Nhận xét trung thực về giới hạn reproduction | Slide 32 |
| Nên có | Plot loss/PPL hoặc runtime | Slide 30-31 |
| Bonus | Memory comparison hoặc synthetic recall | Slide 31-32 |

### 8.2 Phân Công Thực Nghiệm Theo Thành Viên

| Thành viên | Phần phụ trách | File liên quan đã có | Output cần nộp | Ghi chú cần làm thêm |
|---|---|---|---|---|
| TV1 | Metric và cách diễn giải kết quả | `docs/theory_attention.md`, `docs/paper_summary.md`, `docs/comparison_table.md` | 1 đoạn giải thích PPL/loss/runtime có ý nghĩa gì; nhận xét kết quả nhóm có/không khớp trend paper | Chuẩn bị text cho slide 30-32, tránh nói Hyena "tốt hơn" nếu số liệu không chứng minh |
| TV2 | Model setup và scaling analysis | `models/transformer.py`, `models/hyena.py`, `evaluate.py`, `docs/comparison_table.md` | Bảng cấu hình Transformer-small vs Hyena-small; bảng complexity kỳ vọng; kiểm tra lệnh E2/E3 | Đảm bảo so sánh công bằng: cùng batch size, cùng seq_lens nếu cần, ghi rõ dummy input khi đo runtime |
| TV3 | Data pipeline, chạy train/evaluate, gom số liệu | `data/preprocess.py`, `train.py`, `evaluate.py`, `results/plots/reproduce_runtime.png` | CSV E1/E2/E3, bảng kết quả cuối, plot runtime/loss | Ghi rõ hardware, epochs, batch size, seed nếu có; nếu kết quả ít epoch thì ghi preliminary |

### 8.3 Liên Kết Output Thực Nghiệm

| Đầu ra | Người tạo chính | Người dùng lại | Dùng để làm gì |
|---|---|---|---|
| Dataset/tokenizer/pipeline summary | TV3 | TV1, TV2 | TV1 giải thích LM/PPL; TV2 kiểm tra model input shape |
| Bảng model config | TV2 | TV3 | TV3 đưa vào slide setup và đảm bảo lệnh chạy đúng model |
| CSV train/evaluate E1 | TV3 | TV1 | TV1 viết nhận xét PPL/loss, so với paper ở mức xu hướng |
| CSV scaling E2/E3 | TV3 + TV2 | TV2 | TV2 phân tích scaling runtime/memory và liên hệ complexity |
| Plot kết quả | TV3 | Cả nhóm | Dùng ở slide 30-31 và Q&A |
| Nhận xét giới hạn | TV1 + TV2 + TV3 | Cả nhóm | Dùng ở slide 32 và phần hỏi đáp |

### 8.4 Thực Nghiệm Nên Chạy

| ID | Mục tiêu | Lệnh/output mong muốn | Trạng thái hiện tại |
|---|---|---|---|
| E1 | So sánh PPL/loss sau train | `results/E1_transformer_L256.csv`, `results/E1_hyena_L256.csv` | Cần chạy/chốt số |
| E2 | Đo runtime/memory Transformer theo L | `results/E2_transformer_scale.csv` | Cần chạy/chốt số |
| E3 | Đo runtime/memory Hyena theo L | `results/E3_hyena_scale.csv` | Cần chạy/chốt số |
| Plot | Vẽ biểu đồ runtime/loss | `results/plots/reproduce_runtime.png` hoặc plot mới | Đã có 1 plot runtime, cần kiểm tra có khớp số mới không |

### 8.5 Lệnh Gợi Ý

```bash
# E1: train hai model tại L=256
python train.py --model transformer --seq_len 256 --epochs 5 --batch_size 16
python train.py --model hyena --seq_len 256 --epochs 5 --batch_size 16

# E2/E3: scaling runtime/memory, không cần checkpoint
python evaluate.py --model transformer --scaling --seq_lens 256 512 1024 --batch_size 8
python evaluate.py --model hyena --scaling --seq_lens 256 512 1024 2048 --batch_size 8
```

Nếu không đủ GPU/thời gian, giảm `epochs`, `batch_size`, hoặc chỉ chạy `seq_lens 256 512 1024` cho cả hai model. Khi đưa lên slide phải ghi rõ là **preliminary result** nếu số epoch ít hoặc chạy trên CPU/MPS thay vì GPU.

### 8.6 Cách Trình Bày Nếu Kết Quả Không Đẹp

Không cần cố làm kết quả "đẹp". Với reproduction quy mô nhỏ, điều quan trọng là nói trung thực:

- PPL/loss ở scale nhỏ có thể chưa cho thấy Hyena vượt Transformer.
- Hyena pure PyTorch có thể chậm ở sequence ngắn vì overhead FFT.
- Lợi thế của Hyena rõ hơn ở sequence length lớn và implementation tối ưu.
- Kết quả nhóm là minh họa xu hướng, còn kết luận scale lớn dựa trên paper gốc.

---

## 9. Output Chung Sau 3 Tuần

| Output chung | Yêu cầu |
|---|---|
| Slide final | Khoảng 33 slide, chia 11 slide/người, trình bày trong 45 phút |
| Speaker notes final | Mỗi slide có ý chính cần nói, không đọc nguyên văn slide |
| Bản liên kết nội dung | 1 trang tóm tắt mạch: problem -> Hyena method -> paper results -> reproduction |
| File Q&A final | Cả nhóm cùng cập nhật, 15-20 câu hỏi có đáp án, chia theo lý thuyết/method/reproduction |
| Bảng phân công hỏi đáp | Cả nhóm thống nhất, câu hỏi thuộc phần nào thì ai trả lời trước |
| Backup | PDF slide, source slide, repo code, hình ảnh, bảng kết quả |

Output tối thiểu để sẵn sàng present:

| Mức ưu tiên | Output |
|---|---|
| Bắt buộc | Slide 1-22 trình bày đúng bài báo gốc |
| Bắt buộc | Slide 23-29 trình bày scope/setup reproduction |
| Bắt buộc | Slide 30-31 có kết quả hoặc preliminary result |
| Bắt buộc | 15 câu Q&A |
| Nên có | Plot loss/runtime/memory |
| Nên có | Speaker notes đầy đủ |
| Bonus | Demo chạy code nếu chắc chắn ổn định |

---

## 10. Chuẩn Bị Cho 15 Phút Hỏi Đáp

### Câu hỏi về Motivation và Transformer

1. **Vì sao Self-Attention là `O(L^2)`?**  
   Vì cần tính tương quan giữa mọi cặp token, tạo ma trận kích thước `L x L`.

2. **FlashAttention có giải quyết triệt để `O(L^2)` không?**  
   Không. FlashAttention tối ưu bộ nhớ và truy cập bộ nhớ, nhưng số phép tính vẫn là `O(L^2)`.

3. **Vì sao long-context quan trọng trong NLP?**  
   Vì nhiều bài toán cần đọc tài liệu dài, code dài, hội thoại dài, sách, hoặc chuỗi sinh học.

### Câu hỏi về Hyena

4. **Hyena có phải là xấp xỉ attention không?**  
   Không. Hyena không xấp xỉ trực tiếp attention matrix mà xây một operator mới có các tính chất tương tự attention.

5. **Gating trong Hyena có vai trò gì?**  
   Gate phụ thuộc vào input, giúp mô hình chọn lọc thông tin theo nội dung chuỗi.

6. **Long convolution khác CNN thông thường như thế nào?**  
   CNN thường dùng kernel ngắn/local, còn Hyena dùng filter dài bằng toàn bộ sequence.

7. **Tại sao FFT giúp convolution nhanh hơn?**  
   Theo convolution theorem, convolution trong miền thời gian có thể tính bằng nhân element-wise trong miền tần số, với chi phí `O(L log L)`.

8. **Implicit filter là gì?**  
   Thay vì học trực tiếp vector filter dài L, Hyena dùng một FFN nhỏ nhận positional encoding để sinh giá trị filter theo vị trí.

### Câu hỏi về kết quả bài báo

9. **Bài báo chứng minh Hyena tốt hơn Transformer không?**  
   Không phải tốt hơn mọi mặt. Bài báo cho thấy Hyena có thể match Transformer quality ở một số setting và nhanh hơn rõ khi sequence length lớn.

10. **Hyena mạnh nhất ở đâu?**  
    Ở long-context efficiency: runtime/memory tốt hơn khi chuỗi rất dài.

11. **Hạn chế của Hyena là gì?**  
    Cần kernel FFTConv tối ưu, có overhead ở sequence ngắn, training ở scale nhỏ có thể nhạy với hyperparameter.

### Câu hỏi về reproduction của nhóm

12. **Vì sao nhóm không train trên The Pile như paper?**  
    The Pile rất lớn, paper dùng mô hình và tài nguyên vượt phạm vi môn học. Nhóm dùng WikiText-2 để kiểm chứng xu hướng.

13. **Kết quả nhóm có tái hiện đúng paper không?**  
    Nhóm không tái hiện số tuyệt đối; mục tiêu là small-scale reproduction/trend verification.

14. **Nếu Hyena không nhanh hơn trong kết quả nhóm thì sao?**  
    Có thể do sequence length chưa đủ lớn, implementation pure PyTorch chưa tối ưu, hoặc overhead FFT lớn ở scale nhỏ.

15. **Perplexity có ý nghĩa gì?**  
    Perplexity đo khả năng dự đoán token tiếp theo của language model; PPL càng thấp thì mô hình càng tốt.

16. **Nhóm học được gì từ bài báo?**  
    Hiểu bottleneck của attention, cách thiết kế operator subquadratic, và cách thực hiện reproduction có giới hạn tài nguyên.

---

## 11. Checklist Trước Ngày Trình Bày

### Nội dung

- [ ] Có khoảng 33 slide, mỗi người khoảng 11 slide.
- [ ] Slide không quá nhiều chữ.
- [ ] Công thức Hyena recurrence hiển thị đúng.
- [ ] Complexity `O(L^2)` và `O(N * L log L)` được giải thích rõ.
- [ ] Có hình minh họa attention matrix.
- [ ] Có hình minh họa Hyena operator.
- [ ] Kết quả bài báo gốc và kết quả nhóm được tách riêng.

### Thực nghiệm

- [ ] Có bảng cấu hình Transformer-small và Hyena-small.
- [ ] Có dataset và preprocessing setup.
- [ ] Có metric PPL/loss cho E1 hoặc ghi rõ preliminary.
- [ ] Có runtime scaling cho E2/E3 hoặc ghi rõ lý do chưa chạy.
- [ ] Có file CSV/bảng số liệu đi kèm với plot.
- [ ] Có giải thích trung thực nếu kết quả chưa mạnh.

### Trình bày

- [ ] Tập dưới 45 phút.
- [ ] Mỗi người nói khoảng 15 phút.
- [ ] Có câu chuyển ý giữa các thành viên.
- [ ] Có bản PDF offline.
- [ ] Có repo/code/plot backup.
- [ ] Có file Q&A.
- [ ] Mỗi thành viên đã điền phần Q&A của mình.
- [ ] Cả nhóm đã thống nhất bảng phân công trả lời Q&A.

---

## 12. Nguyên Tắc Khi Trả Lời Câu Hỏi

1. Câu hỏi về Transformer/Attention/related work: TV1 trả lời trước.
2. Câu hỏi về Hyena operator/FFT/implicit filter: TV2 trả lời trước.
3. Câu hỏi về code/dataset/kết quả nhóm: TV3 trả lời trước.
4. Nếu không chắc, trả lời trung thực:

> "Trong phạm vi nhóm, chúng em hiểu điểm này ở mức ...; phần chứng minh/toi ưu sâu hơn nằm ngoài scope reproduction, nhưng paper gốc giải thích trong Section ..."

5. Luôn tách bạch:

- "Kết quả bài báo gốc" là của Poli et al.
- "Kết quả của nhóm" là small-scale reproduction.
- "Nhận xét/diễn giải" không phải kết quả đã chứng minh.

---

## 13. File Cần Hoàn Thiện Trong Repo

| File | Mục đích | Phụ trách |
|---|---|---|
| `slides/slide_outline.md` | Outline slide chính | Cả nhóm |
| `slides/slides.md` | Bản Marp tham khảo; cần cập nhật theo outline 33 slide nếu dùng để trình chiếu | Cả nhóm |
| `docs/paper_summary.md` | Tóm tắt paper | TV1 |
| `docs/theory_attention.md` | Nền tảng Transformer | TV1 |
| `docs/comparison_table.md` | So sánh Transformer vs Hyena | TV1 |
| `docs/related_work_notes.md` | Related work | TV1 |
| `README.md` | Hướng dẫn repo và reproduction | TV3 |
| `results/E1_transformer_L256.csv` | Kết quả train/evaluate Transformer | TV3 |
| `results/E1_hyena_L256.csv` | Kết quả train/evaluate Hyena | TV3 |
| `results/E2_transformer_scale.csv` | Runtime/memory Transformer theo sequence length | TV3 |
| `results/E3_hyena_scale.csv` | Runtime/memory Hyena theo sequence length | TV3 |
| `results/plots/reproduce_runtime.png` | Hình kết quả | TV3 |

---

## 14. Tóm Tắt 1 Phút Để Mở Đầu Hoặc Kết Bài

> Bài báo *Hyena Hierarchy* đặt câu hỏi liệu attention có phải thành phần bắt buộc để xây dựng mô hình ngôn ngữ mạnh hay không. Điểm yếu của Self-Attention là chi phí `O(L^2)`, khiến việc xử lý chuỗi dài rất tốn kém. Hyena đề xuất một operator không dùng attention, kết hợp long convolution qua FFT và element-wise gating, đạt chi phí subquadratic `O(N * L log L)` nhưng vẫn giữ các tính chất quan trọng của attention như data control và unrestricted context. Paper cho thấy Hyena có thể đạt chất lượng gần Transformer trên các benchmark lớn và nhanh hơn rõ rệt khi sequence length dài. Trong phạm vi môn học, nhóm thực hiện small-scale reproduction trên WikiText-2 để kiểm chứng xu hướng giữa Transformer-small và Hyena-small về perplexity, runtime và khả năng scale theo sequence length.
