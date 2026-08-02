# Speaker Notes Của Tiến - Chi Tiết

Mục tiêu thời gian: **15 phút cho phần Tiến trong deck hiện tại**.  
Toàn bộ số slide trong file này được ghi theo đúng **stt góc dưới bên phải của deck**, tức dạng **`x/38`**.

Mốc nói thực tế:

1. **17/38**: slide phân cách `Cơ chế Hyena` - có thể nói 1 câu chuyển ý rất ngắn.
2. **18/38-23/38**: phần cơ chế Hyena.
3. **24/38**: slide phân cách `Hiện thực hiệu quả & Kết quả paper` - tiếp tục chuyển ý.
4. **25/38-29/38**: phần hiện thực, độ phức tạp và kết quả paper.

Nhịp nói hợp lý: **60-75 giây/slide nội dung**, riêng slide **22/38, 26/38, 27/38, 28/38** có thể kéo lên **80-90 giây**.

Mục tiêu của phần Tiến:

1. Giải thích **Hyena hoạt động như thế nào**.
2. Làm rõ **vì sao Hyena rẻ hơn Attention khi chuỗi dài**.
3. Tách bạch **kết quả paper gốc** với **phần reproduction của nhóm**.

Thông điệp toàn phần nên giữ xuyên suốt:

> Hyena không xấp xỉ trực tiếp attention matrix. Thay vào đó, nó xây một operator mới bằng long convolution, gating, implicit filter và FFT để giữ khả năng mô hình hóa phụ thuộc xa với chi phí subquadratic.

Sau khi đối chiếu với paper gốc `docs/poli23a.pdf`, phần nói của Tiến nên bám vào 4 điểm neo:

1. Paper thiết kế Hyena để giữ lại **3 tính chất quan trọng của attention**: data control, unrestricted context, và parameter count không phụ thuộc trực tiếp vào sequence length.
2. Hyena operator được định nghĩa ở **Definition 3.1** bằng recurrence `z^(n+1)_t = x^n_t * (h^n * z^n)_t`.
3. Algorithm trong paper có thêm **short depthwise convolution trên các projection** trước khi split thành `x1...xN, v`; slide đã giản lược điểm này để tập trung vào operator chính.
4. Kết quả runtime của paper nên nói đúng số: khoảng **5x so với attention và 2x so với FlashAttention ở 8192 token**, và khoảng **100x so với FlashAttention ở 64K token**.

---

## Quy Ước Cách Đọc Khi Nói

Phần này để đọc trôi miệng khi gặp công thức, ký hiệu và viết tắt trên slide.

### Viết tắt nên đọc thế nào

- `FFT`: khi nói nên đọc là "biến đổi Fourier nhanh"
- `iFFT`: khi nói nên đọc là "biến đổi Fourier ngược"
- `FFN`: khi nói nên đọc là "mạng truyền thẳng" hoặc "mạng feed-forward"
- `CNN`: khi nói nên đọc là "mạng tích chập"
- `SSM`: khi nói nên đọc là "mô hình không gian trạng thái"
- `H3`: khi nói nên đọc là "mô hình H ba"
- `GSS`: khi nói nên đọc là "mô hình GSS"
- `FlashAttention`: khi nói nên đọc là "FlashAttention, tức attention được tối ưu cách truy cập bộ nhớ"
- `WikiText-103`: khi nói nên đọc là "bộ dữ liệu WikiText một không ba"
- `WikiText-2`: khi nói nên đọc là "bộ dữ liệu WikiText hai"
- `The Pile`: khi nói nên đọc là "bộ dữ liệu The Pile"

### Độ phức tạp nên đọc thế nào

- `O(L^2)`: khi nói nên đọc là "độ phức tạp tỷ lệ theo L bình phương"
- `O(L log L)`: khi nói nên đọc là "độ phức tạp cỡ L log L"
- `O(N * L log L)`: khi nói nên đọc là "độ phức tạp cỡ N nhân L log L"
- `subquadratic`: khi nói nên đọc là "thấp hơn bậc hai theo độ dài chuỗi"

### Ký hiệu thường gặp nên đọc thế nào

- `L`: khi nói nên đọc là "độ dài chuỗi"
- `N`: khi nói nên đọc là "số bậc của Hyena" hoặc "số lần lặp"
- `x^n`: khi nói nên đọc là "gate ở bước n"
- `z^n`: khi nói nên đọc là "trạng thái trung gian ở bước n"
- `h^n`: khi nói nên đọc là "filter ở bước n"
- `x^n_t`: khi nói nên đọc là "gate tại vị trí t ở bước n"
- `z^(n+1)`: khi nói nên đọc là "trạng thái ở bước kế tiếp"
- `h_t`: khi nói nên đọc là "giá trị filter tại vị trí t"
- `L x L`: khi nói nên đọc là "ma trận kích thước L nhân L"

### Tên toán học nên đọc đơn giản

- `Toeplitz matrix`: khi nói nên đọc là "ma trận tích chập có cấu trúc lặp"
- `diagonal matrix`: khi nói nên đọc là "ma trận đường chéo"
- `element-wise`: khi nói nên đọc là "nhân theo từng phần tử"
- `causal convolution`: khi nói nên đọc là "tích chập chỉ nhìn về quá khứ"
- `positional encoding`: khi nói nên đọc là "mã hóa vị trí"

### Dễ nhầm: FFN khác FFT

- `FFN` là **Feed-Forward Network**, tức một mạng neural nhỏ dùng để sinh giá trị filter từ positional encoding.
- `FFT` là **Fast Fourier Transform**, tức phép biến đổi toán học dùng để tính convolution nhanh hơn.
- Câu nhớ nhanh: **FFN sinh filter, FFT tính convolution**.

---

## Slide 17/38 - Divider: Cơ chế Hyena

**Mục tiêu slide:** Đánh dấu Tiến bắt đầu và nhận bàn giao từ TV1.

**Lời thoại rất ngắn gợi ý:**

"Ở phần trước, chúng ta đã thấy vì sao attention rất mạnh nhưng bị chặn bởi chi phí `O(L^2)`. Tiếp theo, mình sẽ trình bày cơ chế Hyena, tức là cách bài báo thay self-attention bằng một operator attention-free có chi phí tốt hơn cho chuỗi dài."

**Câu chuyển sang slide 18/38:**

"Mình bắt đầu từ câu hỏi: Hyena thực ra thay attention bằng cái gì?"

---

## Slide 18/38 - Từ Attention Sang Hyena

**Mục tiêu slide:** Chuyển mạch từ vấn đề của Attention sang động cơ ra đời của Hyena.

**Lời thoại gợi ý:**

"Ở phần trước, chúng ta đã thấy Self-Attention rất mạnh vì có thể trộn thông tin giữa mọi cặp token. Tuy nhiên, cái giá phải trả là chi phí tính toán và bộ nhớ tăng theo `O(L^2)`, nên khi sequence dài lên vài nghìn hay vài chục nghìn token thì đây trở thành nút thắt rất lớn.

Vì vậy, câu hỏi mà bài báo đặt ra là: liệu có thể xây một toán tử không dùng attention, nhưng vẫn giữ được khả năng xử lý phụ thuộc xa và vẫn đủ mạnh cho language modeling hay không?

Liên hệ với slide trước của Kiên, paper nêu ba tính chất cần giữ lại từ attention: thứ nhất là **data control**, tức phép trộn phụ thuộc vào input; thứ hai là **unrestricted context**, tức có thể nối thông tin ở khoảng cách rất xa; và thứ ba là **sublinear parameter scaling**, tức số tham số không tăng trực tiếp theo độ dài chuỗi.

Hyena là câu trả lời của paper này. Điểm quan trọng là Hyena không cố xấp xỉ trực tiếp ma trận attention. Thay vào đó, nó thiết kế một operator hoàn toàn khác, dựa trên hai thành phần chính là long convolution và data-controlled gating."

**Đoạn nói box và bảng trên slide:**

"Box trên slide là câu hỏi trung tâm của phần này: Hyena thay self-attention bằng toán tử nào, và vì sao rẻ hơn khi context dài?

Mình đọc bảng theo từng dòng. Attention trộn thông tin toàn chuỗi nhưng phải tạo ma trận `L x L`; Hyena thay phần trộn đó bằng long convolution. Attention có trọng số phụ thuộc nội dung; Hyena giữ tinh thần này bằng data-controlled gating. Cuối cùng, attention tốn `O(L^2)` trên context dài, còn long convolution của Hyena được tính bằng FFTConv nên còn khoảng `O(L log L)` cho mỗi convolution."

**Câu nhấn mạnh nên nói chậm:**

> Hyena là một attention-free operator, không phải một bản attention rút gọn.

**Câu chuyển sang slide 19/38:**

"Vậy hai thành phần cốt lõi đó là gì, và vì sao kết hợp của chúng lại đủ mạnh?"

---

## Slide 19/38 - Ý Tưởng Chính Của Hyena

**Mục tiêu slide:** Cho người nghe trực giác tổng quan trước khi vào công thức.

**Lời thoại gợi ý:**

"Ý tưởng chính của Hyena có thể tóm gọn trong một câu: dùng **long convolution** để mang thông tin từ xa, và dùng **gating** để quyết định thông tin nào thực sự nên đi tiếp.

Long convolution cho phép mỗi vị trí nhìn được toàn bộ chuỗi, nên nó đóng vai trò cung cấp global context. Nhưng nếu chỉ có convolution thì phép biến đổi này khá tĩnh, tức là cùng một filter áp lên mọi input.

Vì vậy Hyena thêm gating. Gate được sinh ra từ chính input, rồi nhân element-wise với đầu ra của convolution. Nhờ đó, phép biến đổi trở nên phụ thuộc dữ liệu, gần hơn với tinh thần của attention.

Khi lặp lại nhiều bước convolution cộng gating như vậy, ta có cái gọi là Hyena hierarchy."

**Đoạn nói pipeline trên slide:**

"Đoạn pipeline trên slide nên đọc chậm theo đúng thứ tự.

Đầu tiên, input của block là `u`. Từ `u`, Hyena dùng các linear projection để tách ra nhiều nhánh: các gate `x1` đến `xN`, và nhánh value `v`.

Ở đây `v` là nhánh giá trị ban đầu, còn `x1` đến `xN` là các gate sẽ dùng ở từng bước recurrence.

Trong Algorithm 1 của paper, các projection này còn đi qua một short depthwise convolution trước khi split. Trên slide mình có thể bỏ qua chi tiết này khi nói chính, vì slide đang muốn nhấn mạnh luồng operator cốt lõi.

Sau đó ta khởi tạo:

`z1 = v`

Nghĩa là trạng thái đầu tiên của Hyena lấy từ nhánh `v`.

Tiếp theo, mô hình lặp công thức:

`z(n+1) = x(n) * Conv(h(n), z(n))`

Đọc bằng lời là: ở bước `n`, lấy trạng thái hiện tại `z(n)`, cho đi qua long convolution với filter `h(n)`, rồi nhân element-wise với gate `x(n)`.

Sau vài bước như vậy, trạng thái cuối cùng được đưa ra thành output `y`."

**Ví dụ trực giác nên nói sau pipeline:**

"Có thể hiểu `v` là dòng thông tin chính đang được xử lý. Các gate `x1` đến `xN` giống như các tín hiệu điều khiển được sinh từ cùng input `u`. Mỗi vòng convolution đưa thông tin xa vào `z`, còn gate quyết định thông tin đó có nên đi tiếp mạnh hay yếu.

Vì vậy slide này không nên hiểu là Hyena chỉ có convolution. Ý đúng là: convolution cho khả năng nhìn xa, gating làm việc nhìn xa đó phụ thuộc vào input."

**Trực giác ngắn nên chốt:**

- Convolution: "mang thông tin đi xa"
- Gating: "chọn thông tin nào được giữ lại"

**Câu chuyển sang slide 20/38:**

"Trước tiên, mình đi vào thành phần đầu tiên là long convolution."

---

## Slide 20/38 - Long Convolution

**Mục tiêu slide:** Làm rõ long convolution khác CNN thường ở đâu và vì sao nó quan trọng.

**Cách đọc khi nói:**

- `CNN`: nên nói là "mạng tích chập"
- `L`: nên nói là "độ dài chuỗi"
- Nếu có nhắc công thức convolution: đọc ý nghĩa, không cần đọc từng ký hiệu
- `L x L`: nên nói là "ma trận kích thước L nhân L"

**Lời thoại gợi ý:**

"Trong CNN truyền thống, kernel thường ngắn, ví dụ chỉ bao phủ vài vị trí lân cận. Điều đó rất tốt cho local pattern, nhưng không thuận lợi nếu ta cần học các phụ thuộc rất xa trong chuỗi văn bản.

Hyena đi theo hướng khác: filter của nó có thể dài bằng toàn bộ sequence length `L`. Điều này có nghĩa là một token ở hiện tại có thể nhận tín hiệu từ rất xa về trước thông qua phép tích chập.

Nói đơn giản, thay vì chỉ nhìn cửa sổ nhỏ quanh một token, Hyena cho phép lan truyền thông tin trên toàn chiều dài chuỗi. Với language modeling, đây là causal convolution, nên token hiện tại nhận thông tin từ quá khứ xa chứ không nhìn sang tương lai.

Tuy nhiên, nếu tính long convolution trực tiếp trong miền thời gian thì chi phí vẫn cao. Do đó, long convolution chỉ thực sự hữu ích khi đi kèm một cách tính hiệu quả hơn, và phần đó sẽ xuất hiện ở slide FFTConv."

**Đoạn nói hai box CNN thường / Hyena:**

"Hai box ở giữa slide chỉ để so sánh receptive field. CNN thường dùng kernel ngắn nên chủ yếu bắt pattern gần. Còn Hyena dùng filter dài bằng sequence, nên token hiện tại có thể nhận tín hiệu từ rất xa phía trước. Điểm này không có nghĩa Hyena giống attention, mà chỉ là nó có một cách khác để mở rộng context."

**Đoạn nói công thức/ví dụ trên slide:**

"Nếu cần nói bằng một công thức đơn giản, output tại vị trí `t` có thể hiểu là tổng có trọng số của các token trước đó:

`y_t = h_0*x_t + h_1*x_(t-1) + h_2*x_(t-2) + ...`

Ở đây các hệ số `h_0`, `h_1`, `h_2` là filter. `h_0` quyết định token hiện tại ảnh hưởng bao nhiêu, `h_1` quyết định token ngay trước đó ảnh hưởng bao nhiêu, và nếu filter rất dài thì `h_1000` có thể quyết định token cách 1000 bước ảnh hưởng bao nhiêu.

Điểm chính là: với kernel ngắn như CNN thường, ta chỉ có vài hệ số gần hiện tại. Với long convolution, filter có hệ số cho rất nhiều khoảng cách, nên receptive field có thể phủ toàn chuỗi."

**Điểm cần tránh nói quá đà:**

- Không nói convolution "giống hệt attention".
- Chỉ nên nói nó giúp **truy cập ngữ cảnh dài** theo cách có cấu trúc.

**Câu chuyển sang slide 21/38:**

"Nhưng chỉ có nhìn xa thôi vẫn chưa đủ. Mô hình còn cần biết thông tin xa nào là quan trọng với từng input cụ thể."

---

## Slide 21/38 - Data-Controlled Gating

**Mục tiêu slide:** Giải thích vì sao gating là điểm giúp Hyena vượt convolution tĩnh.

**Cách đọc khi nói:**

- `x^n`: nên nói là "gate ở bước n"
- `input`: nên nói là "đầu vào"
- `element-wise`: nên nói là "theo từng phần tử"

**Lời thoại gợi ý:**

"Nếu chỉ dùng convolution, filter thường khá cố định sau khi học xong. Nghĩa là với hai câu khác nhau, cách tổng hợp thông tin theo thời gian vẫn đi qua cùng một filter. Đây là một hạn chế nếu ta muốn mô hình linh hoạt theo nội dung.

Hyena xử lý điểm này bằng data-controlled gating. Cụ thể, từ input ban đầu, mô hình chiếu ra các tensor `x^n`, và các tensor này sẽ nhân trực tiếp với đầu ra của convolution ở từng bước.

Nhờ đó, dù filter mang thông tin từ xa về, gate sẽ quyết định tín hiệu nào được tăng lên, tín hiệu nào bị làm yếu đi. Có thể hiểu gate đóng vai trò chọn lọc theo ngữ cảnh hiện tại.

Đây là điểm rất quan trọng vì nó làm Hyena khác với convolution thuần: output không còn là một phép biến đổi hoàn toàn tĩnh, mà đã phụ thuộc vào dữ liệu đầu vào."

**Đoạn nói công thức/ví dụ trên slide:**

"Trên slide có ý `gate x^n` nhân với output convolution. Có thể nói đơn giản là:

`new_signal_t = gate_t * conv_output_t`

Nếu `gate_t` nhỏ, tín hiệu sau convolution ở vị trí đó bị giảm. Nếu `gate_t` lớn, tín hiệu được cho đi qua mạnh hơn.

Ví dụ, cùng là thông tin cách 100 token phía trước, nhưng trong câu này nó liên quan đến chủ ngữ chính, còn trong câu khác nó chỉ là chi tiết phụ. Gate giúp mô hình điều chỉnh theo từng input, thay vì dùng cùng một mức ảnh hưởng cố định cho mọi câu."

**Đoạn nói hai box ví dụ số:**

"Hai box số trên slide minh họa phép nhân gate. Bên trái là output sau convolution và gate được sinh từ input. Bên phải là kết quả sau khi nhân từng phần tử. Ví dụ `0.4` nhân với `0.1` thành `0.04`, nghĩa là tín hiệu đó bị giảm mạnh. Còn `0.9` nhân với `0.7` thành `0.63`, nghĩa là tín hiệu vẫn được giữ tương đối nhiều. Gate không phải công tắc 0/1 cứng, mà là hệ số liên tục để điều chỉnh cường độ tín hiệu."

**Ví dụ trực giác ngắn nên thêm khi nói:**

"Trong một đoạn văn dài, không phải thông tin xa nào cũng hữu ích. Gate học cách giữ lại phần liên quan và giảm phần nhiễu."

**Câu chuyển sang slide 22/38:**

"Hai ý tưởng vừa rồi được kết hợp lại trong công thức trung tâm của Hyena."

---

## Slide 22/38 - Hyena Recurrence

**Mục tiêu slide:** Giải thích công thức quan trọng nhất thật rõ ràng, không quá nặng ký hiệu.

**Cách đọc khi nói:**

- `z^(n+1)_t = x^n_t * (h^n * z^n)_t`
  nên nói là: "trạng thái ở bước kế tiếp tại vị trí t bằng gate tại vị trí t nhân với kết quả tích chập giữa filter bước n và trạng thái trung gian bước n"
- `z^n`: nên nói là "trạng thái trung gian ở bước n"
- `h^n`: nên nói là "filter ở bước n"
- `x^n_t`: nên nói là "gate tại vị trí t ở bước n"
- `N`: nên nói là "số bậc" hoặc "số lần lặp"

**Lời thoại gợi ý:**

"Đây là công thức trung tâm của Hyena:

`z^(n+1)_t = x^n_t * (h^n * z^n)_t`

Ta có thể đọc công thức này từng lớp ý nghĩa.

Thứ nhất, `z^n` là trạng thái trung gian ở bước thứ `n`.

Thứ hai, `h^n * z^n` là phép long convolution. Bước này chịu trách nhiệm gom và truyền thông tin dài hạn trong chuỗi.

Thứ ba, `x^n_t` là gate tại vị trí `t`, được sinh từ input. Gate này nhân element-wise với kết quả convolution, nên nó điều khiển lượng thông tin được đi tiếp.

Sau đó kết quả trở thành `z^(n+1)`, và quá trình tiếp tục lặp lại. Nếu lặp `N` lần, ta thu được Hyena order `N`.

Điểm trực giác ở đây là: convolution đóng vai trò memory trên chiều dài chuỗi, còn gate đóng vai trò content-based control."

**Đoạn nói công thức trên slide thật chậm:**

"Công thức này nên đọc từ trong ra ngoài.

Đầu tiên là phần trong ngoặc:

`(h^n * z^n)_t`

Nó nghĩa là: tại vị trí `t`, lấy trạng thái trung gian `z^n`, trộn thông tin dài hạn bằng filter `h^n`, rồi lấy kết quả ở vị trí `t`.

Sau đó mới đến phần bên ngoài:

`x^n_t * (...)`

Nó nghĩa là: dùng gate tại vị trí `t` để nhân vào kết quả convolution. Vì gate này được sinh từ input, nên bước chọn lọc phụ thuộc vào dữ liệu.

Cuối cùng ta thu được:

`z^(n+1)_t`

tức là trạng thái mới tại vị trí `t`. Nếu nói cực ngắn, mỗi bước Hyena là: trộn xa bằng convolution, rồi lọc bằng gate."

**Đoạn nói bảng và pipeline trên slide:**

"Bảng bên trái giúp mình giải nghĩa ký hiệu: `z1 = v` là value stream ban đầu, `h^n` là filter dài ở bước `n`, `x^n_t` là gate tại token `t`, và `N` là số bậc. Pipeline bên phải là cách đọc công thức bằng thao tác: lấy `z(n)`, convolution với `h(n)`, nhân gate `x(n)`, rồi ra `z(n+1)`. Nếu khán giả nhớ được pipeline này thì đã hiểu phần lõi của Hyena."

**Ví dụ nói miệng cho `N = 2`:**

"Nếu `N = 2`, mô hình làm việc này hai lần. Lần đầu trộn thông tin dài hạn từ input hoặc trạng thái ban đầu. Sau đó gate lọc lại. Lần thứ hai tiếp tục trộn trên biểu diễn đã được lọc, nên operator có thể biểu diễn quan hệ phức tạp hơn một convolution đơn."

**Câu nên nói rất rõ:**

> Hyena không chỉ convolution một lần; nó lặp nhiều bước convolution và gating theo dạng recurrence.

**Liên hệ code nếu cần chỉ tay vào repo:**

- `models/hyena.py`
- lớp `HyenaOperator`
- hàm recurrence nằm trong `forward`

**Câu chuyển sang slide 23/38:**

"Từ đó, khái niệm 'hierarchy' trong tên Hyena cũng trở nên rõ hơn."

---

## Slide 23/38 - Order-N Hierarchy

**Mục tiêu slide:** Giải thích "hierarchy" và vai trò của `N`.

**Cách đọc khi nói:**

- `Order-N`: nên nói là "Hyena bậc N"
- `N`: nên nói là "số bậc"
- `order = 2`: nên nói là "mô hình đang dùng hai bước lặp"

**Lời thoại gợi ý:**

"Từ 'hierarchy' trong Hyena nghĩa là operator này có nhiều bậc, hay nhiều tầng recurrence. `N` chính là số lần lặp lại khối convolution cộng gating mà mình vừa mô tả.

Khi `N` tăng, khả năng biểu diễn của operator cũng tăng, vì mô hình có nhiều bước để trộn thông tin dài hạn với điều khiển theo dữ liệu.

Paper cũng đặt Hyena trong một họ kiến trúc rộng hơn. Cụ thể, paper nói H3 tương ứng với Hyena bậc 2, còn GSS tương ứng với Hyena bậc 1 nếu chọn một cách tham số hóa filter cụ thể bằng SSM. Vì vậy có thể nói Hyena tổng quát hóa các hướng này bằng recurrence bậc `N` và filter implicit tự do hơn.

Trong reproduction của nhóm, để giữ mô hình gọn và train được trong phạm vi môn học, ta dùng cấu hình nhỏ với `order = 2`. Tức là mỗi block Hyena lặp hai bước recurrence."

**Đoạn nói ví dụ trên slide:**

"Có thể hình dung `order = 1` giống như một lần convolution rồi gating. `order = 2` là làm thêm một vòng nữa trên trạng thái đã được xử lý. Order cao hơn cho mô hình thêm cơ hội để kết hợp thông tin xa và điều khiển theo nội dung.

Tuy nhiên, mỗi lần tăng order là thêm chi phí, vì phải thêm một bước convolution và một gate. Vì vậy trong repo nhóm, dùng `order = 2` là lựa chọn cân bằng: đủ để minh họa Hyena hierarchy, nhưng vẫn nhỏ để train được."

**Câu chốt ngắn:**

> `N` càng lớn thì operator càng linh hoạt, nhưng chi phí cũng tăng theo.

**Câu chuyển sang slide 24/38:**

"Đến đây là xong phần cơ chế cốt lõi. Tiếp theo mình chuyển sang cách hiện thực Hyena hiệu quả và kết quả paper gốc."

---

## Slide 24/38 - Divider: Hiện thực hiệu quả & Kết quả paper

**Mục tiêu slide:** Chuyển từ cơ chế sang implementation view và kết quả thực nghiệm paper.

**Lời thoại rất ngắn gợi ý:**

"Phần vừa rồi trả lời Hyena hoạt động như thế nào. Phần tiếp theo sẽ trả lời hai câu hỏi còn lại: vì sao nó tính được rẻ hơn, và paper gốc đã chứng minh hiệu quả đó ra sao."

**Câu chuyển sang slide 25/38:**

"Trước hết là một góc nhìn khá quan trọng về mặt cấu trúc ma trận."

---

## Slide 25/38 - Matrix View

**Mục tiêu slide:** Biến phần toán học thành trực giác dễ hiểu.

**Cách đọc khi nói:**

- `Toeplitz`: nên nói là "ma trận tích chập có cấu trúc lặp"
- `diagonal`: nên nói là "ma trận đường chéo"
- `L x L`: nên nói là "L nhân L"
- `dense matrix`: nên nói là "ma trận dày đặc"

**Lời thoại gợi ý:**

"Slide này nhìn hơi toán học, nhưng trực giác lại khá rõ.

Một phép gating element-wise có thể xem như nhân với một **ma trận đường chéo**, vì mỗi vị trí chỉ nhân với hệ số của chính nó.

Còn một phép convolution với cùng filter trượt qua chuỗi có thể xem như nhân với một **ma trận Toeplitz**, tức là ma trận có cấu trúc lặp theo đường chéo.

Vì vậy, toàn bộ Hyena có thể được nhìn như sự xen kẽ giữa các ma trận đường chéo và các ma trận Toeplitz. Điều quan trọng là cả hai loại ma trận này đều có cấu trúc đặc biệt, nên rẻ hơn nhiều so với một ma trận dense `L x L` như attention.

Nói gọn lại, thay vì materialize một attention matrix rất lớn, Hyena dùng một phân rã có cấu trúc nhưng vẫn phụ thuộc dữ liệu thông qua các gate."

**Đoạn nói công thức trên slide:**

"Dòng trên slide có thể đọc như sau:

`Attention: y = A(x) · v`

Nghĩa là attention tạo một ma trận `A` phụ thuộc vào input, rồi dùng nó để trộn các giá trị `v`. Ma trận này là `L x L`, nên rất đắt khi `L` lớn.

Còn Hyena có dạng trực giác:

`Hyena: y ≈ D_x2 · S_h2 · D_x1 · S_h1 · v`

Ở đây `S_h` là phép convolution, tức phần trộn thông tin có cấu trúc. `D_x` là gate, tức phần nhân theo từng vị trí hoặc channel. Hai loại này xen kẽ nhau.

Ý quan trọng là Hyena vẫn tạo được một operator phụ thuộc input nhờ các `D_x`, nhưng không cần tạo một ma trận dense `L x L` như attention."

**Đoạn nói box trên slide:**

"Box trên slide là câu chốt của matrix view: Hyena không tạo trực tiếp một attention matrix dày `L x L`. Thay vào đó, nó xen kẽ hai loại ma trận có cấu trúc: `D_x` từ gating và `S_h` từ convolution. Nhờ vậy operator vẫn phụ thuộc input, nhưng cách tính rẻ hơn vì tận dụng cấu trúc."

**Cách đơn giản hóa nếu khán giả không thích toán:**

"Attention dùng một ma trận lớn, còn Hyena dùng nhiều khối có cấu trúc rẻ hơn để tạo hiệu ứng tổng hợp thông tin."

**Câu chuyển sang slide 26/38:**

"Tuy nhiên, vẫn còn một câu hỏi: filter dài bằng cả sequence thì học nó như thế nào mà không làm số tham số phình ra?"

---

## Slide 26/38 - Implicit Filter

**Mục tiêu slide:** Giải thích vì sao filter dài nhưng số tham số không tăng theo `L`.

**Cách đọc khi nói:**

- `h_t = Window(t) * FFN(PositionalEncoding(t))`
  nên nói là: "giá trị filter tại vị trí t được tạo bằng cách lấy mã hóa vị trí đưa qua một mạng truyền thẳng, rồi nhân với một hàm cửa sổ"
- `h_t`: nên nói là "giá trị filter tại vị trí t"
- `FFN`: nên nói là "mạng truyền thẳng"; đây là mạng neural, không phải FFT
- `PositionalEncoding(t)`: nên nói là "mã hóa vị trí tại t"
- `L`: nên nói là "độ dài chuỗi"

**Lời thoại gợi ý:**

"Đây là một trong những ý tưởng rất hay của Hyena. Nếu ta học trực tiếp một vector filter `h` có độ dài `L`, thì khi `L` tăng, số tham số cũng tăng theo. Điều này không thuận lợi cho long-context.

Hyena tránh cách đó bằng **implicit filter**. Thay vì lưu sẵn mọi phần tử của filter, mô hình học một hàm nhỏ để sinh filter theo từng vị trí:

`h_t = Window(t) * FFN(PositionalEncoding(t))`

Nói dễ hiểu hơn: với mỗi khoảng cách `t`, positional encoding giống như cách ta đưa thông tin "đây là vị trí bao xa" vào mô hình. FFN nhỏ sẽ học trả lời câu hỏi: ở khoảng cách này, tín hiệu nên đi qua mạnh hay yếu? Kết quả đó chính là giá trị filter `h_t`. Còn `Window(t)` giống như một lớp kiểm soát thêm, giúp tín hiệu ở các khoảng cách xa không dao động quá mạnh và làm filter ổn định hơn.

Chỗ này cần phân biệt rõ: `FFN` là mạng neural dùng để **sinh filter**. Nó không phải `FFT`. `FFT` sẽ xuất hiện ở slide sau để **tính convolution nhanh**.

Điểm quan trọng là số tham số của FFN không tăng trực tiếp theo sequence length. Nghĩa là ta có thể sinh filter rất dài mà không cần lưu một vector tham số dài tương ứng.

Trong code của nhóm, phần này nằm ở lớp `HyenaFilter`, nơi positional encoding đi qua FFN rồi được nhân với decay window."

**Đoạn nói công thức/ví dụ trên slide:**

"Công thức trên slide là:

`h_t = Window(t) * FFN(PositionalEncoding(t))`

Mình đọc chậm là: giá trị filter tại vị trí `t` được sinh bằng cách lấy mã hóa vị trí `t`, đưa qua một mạng feed-forward, rồi nhân với một hàm window.

Ví dụ nếu cần filter dài 4096, ta đưa các vị trí từ 0 đến 4095 vào hàm này để sinh ra 4096 giá trị filter. Nếu cần filter dài hơn, ví dụ 8192, ta tiếp tục lấy thêm các vị trí đến 8191. Tham số học vẫn nằm trong FFN, không phải mỗi vị trí có một tham số riêng.

Vì vậy implicit filter giống như học một công thức sinh filter, thay vì học một bảng filter cố định."

**Đoạn nói bảng và pipeline trên slide:**

"Bảng trên slide so sánh hai cách học filter. Nếu explicit thì ta lưu trực tiếp `h[0...L-1]`; khi muốn filter dài hơn, số tham số cũng dễ tăng theo. Còn implicit thì tham số nằm trong FFN, FFN nhận vị trí `t` rồi sinh ra `h_t`.

Pipeline bên dưới đọc theo thứ tự: lấy position `t`, đưa qua positional encoding, qua small FFN để ra raw filter value, rồi nhân với `Window(t)` để ra giá trị filter cuối cùng. `Window` ở đây giúp filter ổn định hơn, đặc biệt ở các khoảng cách xa."

**Câu chốt nên nhấn:**

> Hyena học "quy luật sinh filter", không học từng phần tử filter một cách explicit.

**Câu chuyển sang slide 27/38:**

"Sau khi đã có filter dài, bước tiếp theo là làm thế nào tính convolution đủ nhanh."

---

## Slide 27/38 - FFTConv

**Mục tiêu slide:** Giải thích vì sao convolution dài có thể rơi về `O(L log L)`.

**Cách đọc khi nói:**

- `FFTConv`: nên nói là "tích chập được tính bằng biến đổi Fourier nhanh"
- `FFT`: nên nói là "biến đổi Fourier nhanh"; đây là phép biến đổi toán học, không phải FFN
- `inverse FFT`: nên nói là "biến đổi Fourier ngược"
- `O(L log L)`: nên nói là "độ phức tạp cỡ L log L"

**Lời thoại gợi ý:**

"Nếu tính long convolution trực tiếp trong miền thời gian, chi phí sẽ rất đắt. Hyena dùng FFT để giải quyết việc này.

Ở slide trước, `FFN` là mạng neural để sinh filter. Còn ở slide này, `FFT` là thuật toán toán học để lấy filter đó và signal đang xử lý, rồi tính convolution nhanh hơn.

Theo convolution theorem, convolution trong miền thời gian tương đương với phép nhân từng phần tử trong miền tần số. Vì vậy quy trình là:

1. Lấy FFT của signal và filter.
2. Nhân chúng element-wise trong frequency domain.
3. Dùng inverse FFT để quay lại miền thời gian.

Nhờ vậy, chi phí giảm xuống còn `O(L log L)` thay vì dạng bậc hai theo `L`.

Trong implementation của nhóm, phần này nằm ở hàm `_causal_fft_conv` trong `models/hyena.py`. Hàm đó dùng zero-padding để bảo toàn linear convolution, sau đó crop lại để giữ tính causal, nghĩa là mỗi token chỉ nhìn về quá khứ."

**Đoạn nói các box trên slide:**

"Box đầu tiên là trực giác chính: đổi miền tính toán để convolution trở thành phép nhân element-wise. Pipeline ở giữa là ba bước thực hiện: FFT signal và filter, nhân trong miền tần số, rồi iFFT để quay lại chuỗi output.

Hai box cuối slide là so sánh chi phí. Direct convolution không phù hợp khi filter rất dài vì phải trượt filter và cộng nhiều lần. FFTConv có overhead, nhưng khi `L` lớn thì chi phí `O(L log L)` tốt hơn nhiều so với cách tính trực tiếp."

**Nếu thầy hỏi chi tiết causal FFT trong paper:**

"Paper nói để bảo toàn causality, chỉ cần evaluate filter ở các vị trí `0` đến `L-1`, rồi zero-pad input và filter lên khoảng `2L-1` trước khi FFT. Sau khi iFFT thì lấy lại phần độ dài `L`. Ý chính là tránh circular convolution làm token hiện tại bị lẫn thông tin tương lai."

**Đoạn nói công thức/ví dụ trên slide:**

"Mình có thể giải thích chậm hơn như sau. Nếu tính trực tiếp convolution dài, tại mỗi vị trí output ta phải tính một tổng dài:

`y_t = h_0*x_t + h_1*x_(t-1) + h_2*x_(t-2) + ...`

Một output cần khoảng `L` phép nhân cộng. Có `L` output, nên tổng gần `O(L^2)`.

FFTConv dùng convolution theorem:

`FFT(x * h) = FFT(x) * FFT(h)`

Điểm mấu chốt là vế phải chỉ là nhân element-wise. Tức là sau khi đổi input và filter sang frequency domain, ta không trượt filter nữa, mà chỉ nhân từng cặp phần tử:

`Y_0 = X_0 * H_0`, `Y_1 = X_1 * H_1`, ...

Sau đó dùng inverse FFT để quay lại sequence output. Vì FFT và inverse FFT tốn `O(L log L)`, nên tổng chi phí convolution dài giảm từ gần `O(L^2)` xuống `O(L log L)`."

**Điểm thực tế nên thêm:**

"Repo của nhóm dùng PyTorch FFT thuần để minh họa đúng cơ chế. Vì vậy nó đủ để thấy xu hướng, nhưng chưa phải implementation tối ưu như các kernel CUDA trong paper."

**Câu chuyển sang slide 28/38:**

"Từ đây, ta mới thấy rõ vì sao Hyena hấp dẫn trong bài toán long-context."

---

## Slide 28/38 - Complexity và Ý Nghĩa

**Mục tiêu slide:** Chốt lợi thế tính toán và nói rõ điều kiện lợi thế này phát huy.

**Cách đọc khi nói:**

- `O(L^2)`: nên nói là "độ phức tạp bậc hai theo độ dài chuỗi"
- `O(N * L log L)`: nên nói là "độ phức tạp cỡ N nhân L log L"
- `FlashAttention`: nên nói là "FlashAttention, một cách tối ưu attention"
- `8K`, `16K`, `64K`: nên nói là "tám nghìn", "mười sáu nghìn", "sáu mươi bốn nghìn token"

**Lời thoại gợi ý:**

"Với attention chuẩn, thời gian và bộ nhớ đều bị ảnh hưởng mạnh bởi ma trận `L x L`, nên thường được mô tả ở mức `O(L^2)`.

Trong khi đó, nếu nhìn theo chiều sequence và coi width là cố định, Hyena có chi phí xấp xỉ `O(N * L log L)`, với `N` là order của recurrence. Paper viết đầy đủ hơn là `O(N * D * L * (log L + D))`, trong đó `D` là model width. Khi tập trung so với attention theo `L`, điểm chính vẫn là `L log L` tăng chậm hơn rất nhiều so với `L^2`.

Ý nghĩa thực tế là Hyena đặc biệt phù hợp khi ta muốn mở rộng lên chuỗi rất dài, ví dụ 8K, 16K, 64K token hoặc hơn.

Tuy nhiên, mình cũng cần nói công bằng rằng ở sequence ngắn, Hyena chưa chắc nhanh hơn. FFT có overhead, và nếu implementation chưa tối ưu thì attention hoặc FlashAttention vẫn có thể thắng ở vùng ngắn. Vì vậy lợi thế của Hyena không phải ở mọi chế độ, mà chủ yếu xuất hiện rõ trong long-context."

**Đoạn nói bảng trên slide:**

"Bảng này nên đọc theo cột `Compute theo L`. Standard Attention là `O(L^2)` vì phải xét các cặp token và tạo ma trận `L x L`. FlashAttention vẫn là `O(L^2)` về compute, nhưng tối ưu IO và memory access nên chạy nhanh hơn attention thường. Hyena khác ở chỗ không tạo attention matrix; chi phí theo `L` là khoảng `O(N * L log L)`, với `N` là số bước recurrence và thường chọn nhỏ."

**Đoạn nói box trên slide:**

"Box ở giữa là ý cần chốt: khi `L` càng lớn, `L log L` tăng chậm hơn `L^2`, nên lợi thế của Hyena chỉ thật sự rõ ở long-context. Vì vậy không nên nói Hyena luôn nhanh hơn, mà nên nói Hyena có điểm rơi ở chuỗi dài."

**Đoạn nói ví dụ số trên slide:**

"Nếu muốn làm rõ trực giác tăng trưởng, có thể lấy ví dụ rất đơn giản. Khi `L` tăng gấp đôi, attention dạng `L^2` có xu hướng tăng khoảng bốn lần về số cặp token cần xét. Còn `L log L` tăng chậm hơn nhiều, gần với tuyến tính hơn.

Đó là lý do ở sequence ngắn, overhead FFT có thể làm Hyena chưa thắng. Nhưng khi context dài lên, phần `L^2` của attention phình rất nhanh, còn Hyena tăng chậm hơn."

**Câu nên nói rất rõ để tránh hiểu nhầm:**

> Subquadratic không có nghĩa là luôn nhanh hơn trong mọi setting; nó có lợi thế rõ nhất khi `L` đủ lớn.

**Câu chuyển sang slide 29/38:**

"Vậy paper gốc đã chứng minh lợi thế này bằng thực nghiệm như thế nào?"

---

## Slide 29/38 - Kết Quả Paper Gốc

**Mục tiêu slide:** Tóm tắt kết quả đủ tự tin nhưng không lẫn với kết quả nhóm.

**Cách đọc khi nói:**

- `WikiText-103`: nên nói là "bộ dữ liệu WikiText một không ba"
- `The Pile`: nên nói là "bộ dữ liệu The Pile"
- `8K`, `64K`: nên nói là "tám nghìn", "sáu mươi bốn nghìn"
- `FlashAttention`: nên nói là "FlashAttention"

**Lời thoại gợi ý:**

"Ở slide cuối phần method, mình chỉ chốt lại các kết quả chính của paper gốc.

Trên các benchmark language modeling như WikiText-103 và The Pile, Hyena cho thấy chất lượng rất gần Transformer, và trong một số setting có thể match baseline attention ở cùng quy mô tham số.

Ngoài chất lượng, điểm nổi bật hơn là hiệu năng trên long-context. Paper benchmark Hyena order 2 với fused CUDA FFTConv. Ở độ dài khoảng 8192 token, Hyena nhanh hơn khoảng 5 lần so với attention thường và khoảng 2 lần so với FlashAttention. Ở 64K token, paper báo cáo mức nhanh hơn khoảng 100 lần so với FlashAttention.

Paper cũng nói điểm giao không xuất hiện ngay ở chuỗi ngắn: Hyena bắt đầu vượt attention quanh 2048 token, và vượt FlashAttention ở khoảng 4096 đến 8192 token. Điều này quan trọng vì nó cho thấy Hyena không chỉ là một ý tưởng lý thuyết, mà có lợi thế thực nghiệm rõ khi context đủ dài."

**Đoạn nói bảng/kết quả trên slide:**

"Khi đọc bảng, mình không cần đi vào toàn bộ số chi tiết. Mình nên gom thành hai ý.

Ý thứ nhất là quality, tương ứng bảng bên trái. Trên WikiText-103, Hyena-3 ở 125M đạt chất lượng gần Transformer 125M. Trên The Pile 335M, Hyena-2 match GPT baseline về perplexity, với khoảng 20% giảm FLOPs ở phần attention-related compute. Với associative recall, paper cho thấy Hyena giữ được khả năng truy xuất trên chuỗi rất dài, trong khi nhiều baseline không fit vào bộ nhớ.

Ý thứ hai là efficiency, tương ứng bảng bên phải. Ở khoảng 2K token là gần điểm giao với attention thường. Ở 8K, Hyena nhanh hơn khoảng 5 lần so với attention thường và khoảng 2 lần so với FlashAttention. Ở 64K, paper báo cáo khoảng 100 lần so với FlashAttention. Đây là phần liên hệ trực tiếp với complexity `O(N * L log L)` đã nói ở slide trước.

Nếu bị hỏi về associative recall, có thể nói đây là synthetic task kiểm tra khả năng nhớ và truy xuất thông tin ở khoảng cách rất xa. Paper dùng nó để cho thấy Hyena không chỉ học tốt language modeling thông thường, mà còn xử lý được phụ thuộc dài hạn."

**Đoạn nói box cuối slide:**

"Box cuối slide là câu kết của phần paper gốc: Hyena vừa thu hẹp quality gap với Transformer, vừa cho thấy lợi thế rõ ở context rất dài. Sau câu này mình chuyển sang phần reproduction của nhóm, nơi nhóm kiểm chứng xu hướng ở quy mô nhỏ hơn."

**Câu chốt ngắn:**

"Tóm lại, paper cho thấy Hyena vừa thu hẹp khoảng cách chất lượng với Transformer, vừa có lợi thế tốc độ rõ hơn khi context đủ dài."

---

## Các Câu Dự Phòng Khi Bị Hỏi

### Nếu bị hỏi: "Hyena có thay thế hoàn toàn attention không?"

Trả lời ngắn:

> Về mặt paper, Hyena được đề xuất như một attention-free operator có thể cạnh tranh với Transformer trong nhiều setting. Nhưng không có nghĩa là nó luôn thay thế attention ở mọi bài toán; điểm mạnh nhất của nó là long-context với chi phí subquadratic.

### Nếu bị hỏi: "Vì sao gating lại làm Hyena gần attention hơn?"

Trả lời ngắn:

> Vì gating làm output phụ thuộc vào input hiện tại. Nếu chỉ convolution thì phép biến đổi khá tĩnh, còn gating tạo ra cơ chế chọn lọc theo nội dung, giống tinh thần data-dependent weighting của attention.

### Nếu bị hỏi: "Hyena có phải SSM không?"

Trả lời ngắn:

> Không hoàn toàn. Hyena có liên hệ với H3, GSS và các hướng SSM trước đó, nhưng paper trình bày nó như một họ operator rộng hơn, dựa trên long convolution, gating và matrix view có cấu trúc.

### Nếu bị hỏi: "Tại sao repo nhóm chưa nhanh hơn Transformer?"

Trả lời ngắn:

> Vì repo này là reproduction nhỏ bằng PyTorch thuần, dùng `torch.fft` thay cho kernel tối ưu như paper. Mục tiêu chính là kiểm chứng cơ chế và xu hướng, không phải tái tạo throughput tuyệt đối ở quy mô công nghiệp.

---

## Nếu Thầy Hỏi: "Phần Này Nằm Ở Đâu Trong Paper?"

Mục này dùng để trả lời nhanh khi bị hỏi nguồn trong bài báo gốc. Không cần đọc nguyên văn section, chỉ cần chỉ đúng vị trí và nói ý chính.

| Chủ đề trong slide Tiến | Nằm ở đâu trong paper | Cách trả lời nhanh |
|---|---|---|
| Motivation: vì sao cần thay attention | **Section 1 - Introduction** | Paper đặt vấn đề attention có chi phí theo `L^2`, nên cần một operator subquadratic nhưng vẫn đủ mạnh cho language modeling. |
| Hyena không phải attention approximation | **Section 1 - Introduction** | Paper không xấp xỉ trực tiếp attention matrix, mà đề xuất một attention-free operator mới. |
| Long convolution + gating | **Section 3 - Hyena Operator** | Phần này định nghĩa Hyena bằng long convolution xen kẽ với các gate phụ thuộc input. |
| Pipeline `u -> x1...xN, v -> z1=v -> recurrence -> y` | **Section 3 - Hyena Operator**, phần định nghĩa operator / algorithm | Đây là luồng tính toán của Hyena operator: input được project thành các gate và value stream, rồi lặp recurrence. |
| Công thức recurrence `z^(n+1)_t = x^n_t * (h^n * z^n)_t` | **Section 3 - Hyena Operator** | Đây là công thức lõi của Hyena: convolution để trộn thông tin dài hạn, gate để điều khiển theo dữ liệu. |
| Order-N / hierarchy | **Section 3 - Hyena Operator** | `N` là số bước recurrence. Paper gọi là hierarchy vì operator có nhiều bậc; các bậc thấp liên hệ với H3/GSS. |
| Matrix view: Diagonal + Toeplitz | **Section 3 - Hyena Operator**, phần matrix decomposition / data-controlled operator | Gating tương ứng với ma trận đường chéo, convolution tương ứng với Toeplitz. Hyena là tích xen kẽ các ma trận có cấu trúc này. |
| Implicit filter `h_t = Window(t) * FFN(PE(t))` | **Section 3 - Hyena Operator**, phần parametrization/filter | Paper dùng implicit filter để sinh long filter từ positional encoding bằng FFN, giúp số tham số không tăng trực tiếp theo sequence length. |
| FFTConv và `O(L log L)` | **Section 3 - Hyena Operator** và phần preliminaries về convolution/FFT | Long convolution được tính bằng FFT: convolution trong time domain thành nhân element-wise trong frequency domain. |
| Causal convolution / zero-padding | **Section 3.4 - Hyena Algorithm**, Proposition 3.1 | Paper nói nếu các filter causal thì Hyena causal; khi dùng FFT thì evaluate filter từ `0` đến `L-1`, zero-pad trước khi FFT để tránh lẫn tương lai. |
| Complexity `O(N * L log L)` | **Section 3.4 - Hyena Algorithm**, Proposition 3.2 | Công thức đầy đủ trong paper là `O(N * D * L * (log L + D))`; trên slide rút gọn theo chiều dài chuỗi thành `O(N * L log L)`. |
| WikiText-103 / The Pile results | **Section 4 - Experiments** | Đây là phần paper báo cáo chất lượng language modeling, so sánh Hyena với Transformer và các attention-free baselines. |
| Speedup ở 8K/64K | **Section 4.4 - Benchmarking** | Paper báo cáo khoảng 5x so với attention và 2x so với FlashAttention ở 8192 token, khoảng 100x so với FlashAttention ở 64K token. |
| Associative recall | **Section 4 - Experiments**, phần long-range/synthetic tasks | Paper dùng tác vụ này để kiểm tra khả năng nhớ và truy xuất thông tin ở khoảng cách rất xa. |
| Related work: H3/GSS/SSM | **Section 2 - Preliminaries/Related background** và discussion trong **Section 3** | H3/GSS là các hướng attention-free trước Hyena; Hyena tổng quát hóa ý tưởng gating + structured sequence mixing. |
| Nếu bị hỏi về Mamba | **Không nằm trong paper gốc** | Mamba xuất hiện sau Hyena, nên chỉ nên nói đây là liên hệ ngoài bài báo, không phải nội dung mà paper Hyena trực tiếp trình bày. |

**Câu trả lời mẫu khi bị hỏi nguồn:**

> "Dạ phần cơ chế này nằm chủ yếu ở Section 3, Hyena Operator. Còn phần kết quả như WikiText-103, The Pile, speedup và associative recall nằm ở Section 4, Experiments."

**Câu nếu không nhớ section nhỏ:**

> "Em nhớ phần method nằm ở Section 3 của paper, còn bảng kết quả và runtime nằm ở Section 4. Em không khẳng định số subsection cụ thể, nhưng đúng mạch là như vậy."

---

## Mẹo Trình Bày

1. Ở slide 22/38, 26/38, 27/38, 28/38 nên nói chậm hơn các slide còn lại vì đây là lõi kỹ thuật.
2. Nếu thiếu thời gian, rút gọn slide 23/38 và 25/38 trước, không nên rút gọn slide 22/38, 26/38, 27/38.
3. Luôn phân biệt ba tầng:
   - **trực giác**: nhìn xa + chọn lọc
   - **công thức**: recurrence
   - **tính toán**: implicit filter + FFT -> subquadratic
4. Ở slide 29/38 phải nói rõ ít nhất một lần:
   - **đây là kết quả paper gốc**
   - **phần reproduction của nhóm nằm ở TV3**
