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
- `FFN`: khi nói nên đọc là "mạng truyền thẳng" hoặc "mạng feed-forward"; nếu đọc từng chữ thì đọc là "ép ép en"
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
- `h[0...L-1]`: khi nói nên đọc là "vector filter h gồm các phần tử từ h không đến h L trừ một"

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

**Lời thoại theo thứ tự trên slide:**

"Ở slide này, em bắt đầu bằng câu hỏi chính: nếu Self-Attention mạnh nhưng bị kẹt ở chi phí `O(L^2)`, thì Hyena thay nó bằng cơ chế nào?

**1. Phần câu hỏi trung tâm**

Vấn đề trung tâm ở đây là: Hyena không cố tạo lại ma trận attention, mà thay bằng một operator không dùng attention. Operator này dựa trên hai ý chính là long convolution và data-controlled gating.

**2. Phần bảng so sánh Attention và Hyena**

Với Attention, mô hình trộn thông tin toàn chuỗi bằng cách xét quan hệ giữa mọi cặp token, nên phải tạo ma trận kích thước `L x L`. Vì vậy khi chuỗi dài, chi phí tăng rất nhanh.

Với Hyena, phần trộn xa được thực hiện bằng long convolution, nên vẫn có unrestricted context, tức vẫn có thể nối thông tin ở khoảng cách rất xa. Sau đó Hyena dùng gating phụ thuộc input để chọn lọc tín hiệu, nên vẫn giữ được data control, tức phép trộn không hoàn toàn cố định mà phụ thuộc dữ liệu.

**3. Phần liên hệ với slide của Kiên**

Liên hệ với **slide 15/38 của Kiên - Khoảng cách năng lực**, paper nói có ba tính chất cần giữ lại từ attention: data control, unrestricted context, và số tham số không tăng trực tiếp theo độ dài chuỗi. Hyena là câu trả lời cho ba yêu cầu đó.

**4. Phần chốt ý**

Câu chốt ở slide này là: Hyena là một attention-free operator, tức là một toán tử không dùng attention. Nó không phải một bản attention rút gọn hay xấp xỉ trực tiếp attention matrix."

**Câu chuyển sang slide 19/38:**

"Vậy operator đó hoạt động cụ thể bằng những bước nào?"

---

## Slide 19/38 - Ý Tưởng Chính Của Hyena

**Mục tiêu slide:** Cho người nghe trực giác tổng quan trước khi vào công thức.

**Lời thoại theo thứ tự trên slide:**

"Slide này tóm tắt ý tưởng chính của Hyena: **long convolution cộng với data-controlled gating**.

**1. Phần hai thành phần chính**

Thành phần thứ nhất là long convolution. Đây là phần giúp mô hình mang thông tin từ xa về. Thay vì token hiện tại chỉ nhìn được một vùng gần, filter dài cho phép thông tin từ các token rất xa phía trước vẫn ảnh hưởng đến output hiện tại. Đây là phần tạo global context.

Nhưng nếu chỉ có convolution thì phép biến đổi còn khá tĩnh, vì một filter học xong sẽ được dùng lại cho nhiều input khác nhau. Vì vậy Hyena thêm thành phần thứ hai là gating. Gate được sinh từ chính input, rồi nhân element-wise với tín hiệu sau convolution. Element-wise ở đây nghĩa là nhân từng phần tử, cụ thể là từng vị trí token và từng channel tương ứng, để quyết định phần tín hiệu nào đi tiếp mạnh hay yếu.

**2. Phần pipeline tổng quát**

Luồng tính toán có thể đọc từ input đến output như sau. Input ban đầu là `u`. Từ `u`, mô hình dùng các linear projection để tách ra nhiều nhánh: các gate từ `x1` đến `xN` và một nhánh value `v`.

Sau đó đặt `z1 = v`, nghĩa là trạng thái đầu tiên lấy từ value stream.

**Tên công thức:** Hyena recurrence - công thức lặp của Hyena, dạng trực giác.

**Cách đọc:** `z(n+1) = x(n) * Conv(h(n), z(n))` đọc là: `z(n+1)`, tức trạng thái ở bước kế tiếp, bằng `x(n)`, tức gate ở bước `n`, nhân với `Conv(h(n), z(n))`, tức kết quả convolution giữa filter `h(n)` và trạng thái hiện tại `z(n)`.

**Giải thích:** Vế trái `z(n+1)` là kết quả sau một vòng xử lý. Vế phải có hai phần: `Conv(h(n), z(n))` là phần long convolution để trộn thông tin xa, còn `x(n)` là gate để lọc kết quả đó. Dấu nhân giữa `x(n)` và kết quả convolution là nhân từng phần tử, tức từng vị trí token và từng channel tương ứng.

**Ý nghĩa:** Mỗi vòng Hyena làm hai việc: convolution để kéo thông tin xa về, rồi gate để chọn phần thông tin nào được giữ lại.

**3. Phần output**

Lặp như vậy qua nhiều bước thì thu được output `y`. Trực giác ngắn là: convolution mang thông tin đi xa, còn gating chọn thông tin nào nên được giữ lại. Khi hai phần này lặp nhiều lần, ta có Hyena hierarchy."

**Câu chuyển sang slide 20/38:**

"Mình đi vào thành phần đầu tiên trước: long convolution."

---

## Slide 20/38 - Long Convolution

**Mục tiêu slide:** Làm rõ long convolution khác CNN thường ở đâu và vì sao nó quan trọng.

**Lời thoại theo thứ tự trên slide:**

"Slide này so sánh convolution thông thường với long convolution của Hyena.

**1. Phần so sánh CNN thường và Hyena**

Với CNN thường, kernel ngắn và chủ yếu nhìn vùng gần. Nghĩa là token hiện tại chỉ nhận tín hiệu từ vài token lân cận, nên cách này tốt cho local pattern, ví dụ cụm từ ngắn hoặc mẫu gần nhau.

Với Hyena, filter có thể dài bằng sequence, tức có thể trải trên toàn bộ độ dài chuỗi `L`. Vì vậy token hiện tại có thể nhận tín hiệu từ rất xa phía trước. Với language modeling, đây là causal convolution, nghĩa là chỉ nhìn về quá khứ, không nhìn sang tương lai.

**2. Phần công thức convolution**

**Tên công thức:** Causal long convolution - tích chập dài nhân quả.

**Cách đọc:** `(h * u)_t = sum h_(t-i) u_i` đọc là: `(h * u)_t`, tức kết quả convolution tại vị trí `t`, bằng tổng của các tích `h_(t-i) u_i`, trong đó mỗi token quá khứ `u_i` được nhân với trọng số filter tương ứng `h_(t-i)`.

**Giải thích:** Vế trái `(h * u)_t` là output sau convolution tại token hiện tại `t`. Trong ngoặc `(h * u)`, `h` là filter, `u` là chuỗi input, và dấu `*` là phép convolution. Vế phải là tổng theo chỉ số `i`; `u_i` là token ở vị trí quá khứ `i`, còn `h_(t-i)` là trọng số filter ứng với khoảng cách từ vị trí `i` đến vị trí hiện tại `t`.

**Ý nghĩa:** Để tạo output ở token hiện tại, mô hình lấy token hiện tại, token ngay trước đó, token trước nữa, và tiếp tục như vậy về quá khứ; mỗi token được nhân với một trọng số trong filter `h`, rồi tất cả được cộng lại.

**3. Phần ví dụ đọc công thức**

Ví dụ dễ đọc hơn là:

`output_t = h0 * token_t + h1 * token_(t-1) + h2 * token_(t-2) + ...`

Nghĩa là `h0` là trọng số cho token hiện tại, `h1` là trọng số cho token ngay trước đó, `h2` là trọng số cho token cách hai bước. Nếu filter đủ dài, thì token cách rất xa, ví dụ cách 1000 bước, vẫn có một trọng số riêng và vẫn có thể đóng góp vào output hiện tại.

Vậy câu nói gọn nhưng đủ ý là: long convolution tạo output hiện tại bằng cách cộng có trọng số nhiều token trong quá khứ, và filter càng dài thì mô hình càng có khả năng lấy thông tin từ xa.

**4. Phần minh họa trực quan**

Có thể hình dung trực quan như sau: CNN vùng gần chỉ nhìn một cửa sổ nhỏ quanh token `t`, còn long convolution có thể kéo thông tin từ xa về token `t`. Điểm cần chốt là Hyena mở rộng context bằng convolution có cấu trúc, chứ không tạo ma trận attention `L x L`."

**Câu chuyển sang slide 21/38:**

"Nhưng chỉ nhìn xa thôi chưa đủ; mô hình còn cần biết thông tin xa nào là quan trọng với từng input."

---

## Slide 21/38 - Data-Controlled Gating

**Mục tiêu slide:** Giải thích vì sao gating là điểm giúp Hyena vượt convolution tĩnh.

**Lời thoại theo thứ tự trên slide:**

"Slide này giải thích thành phần thứ hai là data-controlled gating, tức cơ chế gate được điều khiển bởi dữ liệu đầu vào.

**1. Phần vấn đề của convolution thuần**

Vấn đề là nếu chỉ dùng convolution thuần, mô hình tuy nhìn được xa nhưng cách trộn thông tin vẫn khá cố định. Sau khi filter đã học xong, cùng một filter có thể được áp lên nhiều câu khác nhau. Điều này làm mô hình thiếu linh hoạt, vì trong mỗi câu, phần thông tin quan trọng có thể nằm ở những vị trí khác nhau.

Hyena giải quyết bằng cách sinh gate từ chính input. Có thể hiểu gate là một bộ điều chỉnh tín hiệu: sau khi convolution kéo thông tin xa về, gate sẽ quyết định phần nào nên đi tiếp mạnh hơn, phần nào nên bị giảm xuống.

**2. Phần element-wise**

Phép nhân ở đây là element-wise, tức là nhân từng phần tử tương ứng. Nói cụ thể hơn, tại mỗi vị trí token và mỗi channel, giá trị gate sẽ nhân với giá trị output của convolution ở đúng vị trí và channel đó.

**3. Phần ví dụ số**

Ví dụ số có thể hiểu như sau. Sau bước convolution, giả sử mô hình đã kéo được một số tín hiệu từ context dài về token hiện tại. Các số như `0.4` hay `0.9` đại diện cho độ mạnh của tín hiệu sau convolution. Gate tương ứng, ví dụ `0.1` hay `0.7`, đại diện cho mức độ mô hình muốn cho tín hiệu đó đi tiếp.

Nếu tín hiệu sau convolution là `0.4` nhưng gate chỉ là `0.1`, khi nhân lại ta được `0.04`. Nghĩa là dù convolution có mang tín hiệu đó về, gate vẫn quyết định giảm nó xuống rất mạnh, có thể vì tín hiệu đó không quan trọng trong ngữ cảnh hiện tại.

Ngược lại, nếu tín hiệu sau convolution là `0.9` và gate là `0.7`, kết quả là `0.63`. Tín hiệu này vẫn còn khá lớn sau gating, nghĩa là mô hình đang cho phép thông tin đó tiếp tục đi qua vì nó có vẻ hữu ích hơn.

Nói ngắn gọn, convolution trả lời câu hỏi: thông tin nào từ xa được đưa về? Còn gate trả lời câu hỏi: trong input hiện tại, thông tin đó nên được giữ lại bao nhiêu?

**4. Phần chốt ý**

Điểm quan trọng là gate không phải công tắc bật tắt cứng. Nó là hệ số liên tục để điều chỉnh cường độ tín hiệu. Vì gate phụ thuộc input, Hyena không còn là convolution tĩnh nữa, mà có khả năng chọn lọc thông tin theo nội dung, gần hơn với tinh thần data-dependent của attention.

Câu chốt của slide này là: long convolution giúp nhìn xa, còn gating giúp chọn đúng thông tin xa cần giữ lại."

**Câu chuyển sang slide 22/38:**

"Hai thành phần này được ghép lại trong công thức trung tâm của Hyena."

---

## Slide 22/38 - Hyena Recurrence

**Mục tiêu slide:** Giải thích công thức quan trọng nhất thật rõ ràng, không quá nặng ký hiệu.

**Lời thoại theo thứ tự trên slide:**

"Đây là slide quan trọng nhất về cơ chế.

**1. Phần công thức trung tâm**

**Tên công thức:** Hyena recurrence - công thức lặp lõi của Hyena.

**Cách đọc:** `z^(n+1)_t = x^n_t * (h^n * z^n)_t` đọc là: `z^(n+1)_t`, tức trạng thái mới tại vị trí `t`, bằng `x^n_t`, tức gate tại vị trí `t` ở bước `n`, nhân với mở ngoặc `(h^n * z^n)_t`, tức kết quả long convolution giữa filter bước `n` và trạng thái trung gian bước `n` tại vị trí `t`, rồi đóng ngoặc.

**Giải thích:** Vế trái `z^(n+1)_t` là kết quả sau khi cập nhật trạng thái ở bước kế tiếp, tại token `t`. Vế phải có hai phần. Phần ngoài là `x^n_t`, tức gate tại token `t`. Phần trong ngoặc `(h^n * z^n)_t` là long convolution: `h^n` là filter dài ở bước `n`, `z^n` là trạng thái trung gian hiện tại, dấu `*` trong ngoặc là convolution, và chỉ số `_t` nghĩa là lấy kết quả tại token hiện tại. Sau đó gate `x^n_t` nhân vào kết quả convolution ở cùng vị trí.

**Ý nghĩa:** Mỗi bước Hyena lấy trạng thái hiện tại, trộn thông tin xa bằng convolution, rồi dùng gate để lọc tín hiệu đó. Nếu gate lớn thì tín hiệu sau convolution được giữ mạnh hơn; nếu gate nhỏ thì tín hiệu bị giảm xuống. Kết quả là `z^(n+1)_t`, tức trạng thái mới ở bước kế tiếp tại token `t`.

**2. Phần bảng ký hiệu**

Các ký hiệu cần nhớ là: `z1 = v` là value stream ban đầu; `h^n` là filter dài ở bước `n`; `x^n_t` là gate tại token `t`; và `N` là số bậc, hay số lần lặp recurrence.

**3. Phần pipeline bốn bước**

Quy trình thao tác có thể nói theo đúng bốn bước được đánh số.

Bước 1, bắt đầu từ `z(n)`. Đây là trạng thái hiện tại, tức biểu diễn trung gian mà mô hình đang giữ ở bước thứ `n`.

Bước 2, đưa `z(n)` qua long convolution với filter `h(n)`. Bước này tạo ra một tín hiệu mới đã gom thông tin từ nhiều vị trí trong quá khứ, nên nó chịu trách nhiệm cho phần long-context.

Bước 3, nhân tín hiệu sau convolution với gate `x(n)`. Gate này cũng nằm ở bước `n`, và được sinh từ input, nên nó quyết định phần tín hiệu nào nên được giữ lại mạnh hơn hoặc làm yếu đi.

Bước 4, kết quả sau khi nhân gate trở thành `z(n+1)`, tức trạng thái mới cho bước tiếp theo. Nếu làm quá trình này một lần thì là order 1; làm hai lần thì là order 2; tổng quát nếu lặp `N` lần thì ta có Hyena order `N`.

**4. Phần output và chốt ý**

Câu nói ngắn cho công thức này là: mỗi bước Hyena làm hai việc, trộn xa bằng convolution rồi lọc theo input bằng gate. Vì vậy Hyena không chỉ convolution một lần, mà là một recurrence gồm nhiều bước convolution và gating."

**Câu chuyển sang slide 23/38:**

"Từ recurrence này, chữ hierarchy trong Hyena sẽ rõ hơn."

---

## Slide 23/38 - Order-N Hierarchy

**Mục tiêu slide:** Giải thích "hierarchy" và vai trò của `N`.

**Lời thoại theo thứ tự trên slide:**

"Slide này nói về order-N hierarchy. `N` ở đây là số bậc của Hyena, hay đơn giản là số lần lặp khối convolution cộng gating.

**1. Phần ý nghĩa của order-N**

Khi `N` tăng thì operator có thêm nhiều tầng tương tác có cấu trúc. Order 1 nghĩa là một lần trộn xa rồi gating. Order 2 nghĩa là làm thêm một vòng nữa trên trạng thái đã được xử lý. Order cao hơn cho mô hình thêm cơ hội kết hợp thông tin xa với điều khiển theo nội dung.

**2. Phần liên hệ H3/GSS/SSM**

Paper cũng liên hệ Hyena với các kiến trúc trước đó. H3 có thể xem như một trường hợp gần với Hyena bậc 2, còn GSS gần với Hyena bậc 1 nếu filter được tham số hóa theo SSM. Ở đây `SSM` là State Space Model, tiếng Việt là mô hình không gian trạng thái; nói đơn giản, đây là một hướng attention-free dùng trạng thái ẩn để truyền thông tin theo chuỗi. Ý này không cần chứng minh sâu trên slide; chỉ cần nắm rằng Hyena tổng quát hóa các cách trộn chuỗi có cấu trúc bằng cách thêm nhiều bậc recurrence.

**3. Phần pipeline order**

Có thể hình dung order 1 là một vòng convolution plus gating. Order 2 là hai vòng. Order `N` là lặp `N` vòng. Mỗi vòng thêm một tầng tương tác, nhưng cũng thêm chi phí, nên trong repo nhóm mình dùng `order = 2` để cân bằng giữa minh họa đúng cơ chế và khả năng train trong phạm vi môn học.

**4. Phần chốt ý**

Câu chốt là: hierarchy không phải là một chứng minh phức tạp cần đi sâu, mà là ý rằng mỗi order thêm một tầng xử lý có cấu trúc."

**Câu chuyển sang slide 24/38:**

"Đến đây là xong phần cơ chế cốt lõi; tiếp theo là cách hiện thực hiệu quả và kết quả paper gốc."

---

## Slide 24/38 - Divider: Hiện thực hiệu quả & Kết quả paper

**Mục tiêu slide:** Chuyển từ cơ chế sang implementation view và kết quả thực nghiệm paper.

**Lời thoại theo thứ tự trên slide:**

"Phần vừa rồi trả lời Hyena hoạt động như thế nào. Phần tiếp theo trả lời hai câu hỏi còn lại: vì sao nó tính được rẻ hơn khi chuỗi dài, và paper gốc báo cáo kết quả đó ra sao."

**Câu chuyển sang slide 25/38:**

"Trước hết là góc nhìn operator có cấu trúc, để thấy Hyena khác attention ở cách tổ chức phép tính."

---

## Slide 25/38 - Matrix View

**Mục tiêu slide:** Biến phần toán học thành trực giác dễ hiểu.

**Lời thoại theo thứ tự trên slide:**

"Slide này nhìn Hyena như một operator có cấu trúc, thay vì một ma trận attention dense.

**1. Phần bảng mapping sang dạng ma trận**

Trước hết, có hai thành phần chính cần map sang dạng ma trận.

Thành phần thứ nhất là gating `x^n`. Vì gating là nhân element-wise, tức nhân từng vị trí và từng channel tương ứng, nên nếu viết dưới dạng ma trận thì nó giống một diagonal matrix `D_x`, tức ma trận đường chéo. Trực giác là mỗi vị trí chỉ được nhân với hệ số gate của chính nó.

Thành phần thứ hai là convolution `h^n * z^n`. Nếu viết convolution dưới dạng phép nhân ma trận, nó tương ứng với Toeplitz matrix `S_h`, tức ma trận có cấu trúc lặp theo đường chéo. Trực giác là cùng một filter `h` được trượt qua toàn bộ chuỗi.

**2. Phần box ý chính**

Câu quan trọng là: Hyena xen kẽ `D_x` và `S_h`, thay vì tạo một attention matrix dense `L x L`. Nghĩa là Hyena vẫn có gating phụ thuộc input, nhưng phần trộn chuỗi dùng cấu trúc convolution để tính rẻ hơn.

**3. Phần công thức Attention**

**Tên công thức attention:** Matrix view of attention - góc nhìn ma trận của attention.

**Cách đọc:** `y = A(x) · v` đọc là: `y`, tức output, bằng `A(x)`, tức ma trận attention phụ thuộc input `x`, nhân với `v`, tức value stream.

**Giải thích:** Vế trái `y` là output sau khi trộn thông tin. Vế phải có `A(x)` là ma trận attention được tạo từ input `x`, và `v` là các value cần được trộn. Dấu `·` là phép nhân ma trận. Vấn đề là `A(x)` có kích thước `L x L`, nên rất tốn khi `L` lớn.

**Ý nghĩa:** Attention trộn thông tin linh hoạt vì ma trận phụ thuộc input, nhưng đổi lại phải trả chi phí lớn cho ma trận dense theo độ dài chuỗi.

**4. Phần công thức Hyena**

**Tên công thức Hyena:** Matrix view of Hyena operator - góc nhìn ma trận của toán tử Hyena.

**Cách đọc:** `Hyena: y ≈ D_x2 · S_h2 · D_x1 · S_h1 · v` đọc là: output `y` của Hyena xấp xỉ bằng chuỗi phép nhân gồm `D_x2`, `S_h2`, `D_x1`, `S_h1`, rồi áp lên value `v`. Trong đó `D_x` là gating, còn `S_h` là convolution.

**Giải thích:** Vế trái `y` là output. Vế phải đọc từ phải sang trái khi hiểu phép nhân ma trận: bắt đầu từ `v`, đi qua `S_h1` là convolution thứ nhất, rồi `D_x1` là gate thứ nhất, tiếp theo `S_h2` là convolution thứ hai, rồi `D_x2` là gate thứ hai. `D_x` là ma trận đường chéo sinh từ gate, nên nó lọc tín hiệu theo input. `S_h` là ma trận Toeplitz sinh từ convolution filter, nên nó trộn thông tin theo cấu trúc convolution. Dấu `≈` nhấn mạnh đây là góc nhìn trực giác dạng ma trận, không phải Hyena đang tạo lại attention matrix.

**Ý nghĩa:** Hyena vẫn có operator phụ thuộc dữ liệu nhờ các gate `D_x`, nhưng không cần tạo ma trận attention dense `L x L`; nó dùng các khối có cấu trúc rẻ hơn.

**5. Phần chốt ý**

Câu chốt của slide này là: Attention dùng một ma trận lớn để trộn mọi cặp token; Hyena thay bằng chuỗi diagonal matrix và Toeplitz matrix xen kẽ, nên vẫn giữ được data control nhưng tận dụng cấu trúc để giảm chi phí."

**Câu chuyển sang slide 26/38:**

"Nhưng nếu filter dài bằng cả sequence, ta cần học filter đó như thế nào để số tham số không phình theo `L`?"

---

## Slide 26/38 - Implicit Filter

**Mục tiêu slide:** Giải thích vì sao filter dài nhưng số tham số không tăng theo `L`.

**Lời thoại theo thứ tự trên slide:**

"Slide này trả lời câu hỏi: filter dài thì học bằng cách nào?

Ý chính là Hyena không lưu trực tiếp toàn bộ filter dài như một vector tham số. Thay vào đó, nó học một hàm nhỏ để sinh filter từ vị trí.

**1. Phần công thức**

**Tên công thức:** Implicit filter parametrization - cách tham số hóa filter ngầm, hay cách sinh filter gián tiếp.

**Cách đọc:** `h_t = Window(t) * FFN(PositionalEncoding(t))` đọc là: `h_t`, tức giá trị filter tại vị trí `t`, bằng `Window(t)`, tức hàm cửa sổ tại vị trí `t`, nhân với `FFN(PositionalEncoding(t))`, tức kết quả của FFN sau khi nhận positional encoding của `t`.

**Giải thích:** `h_t` là giá trị filter ở khoảng cách `t`. Có thể hiểu là: nếu một token cách token hiện tại `t` bước, thì `h_t` cho biết tín hiệu từ khoảng cách đó nên ảnh hưởng mạnh hay yếu.

Ở vế phải, `PositionalEncoding(t)` trước hết biến con số vị trí `t` thành một biểu diễn mà mạng neural hiểu được. Sau đó ta đưa biểu diễn vị trí này qua `FFN` để dự đoán một giá trị filter ban đầu. Cuối cùng `Window(t)` nhân vào như một hệ số điều chỉnh, thường để làm tín hiệu ở xa giảm mượt hơn và giúp filter ổn định hơn.

**Ý nghĩa:** Hyena không học một vector filter dài bằng cách lưu từng phần tử riêng. Nó học một hàm sinh filter: đưa vị trí vào thì sinh ra giá trị filter tương ứng.

Ở slide này chỉ cần nói `FFN` là mạng feed-forward nhỏ, tức mạng truyền thẳng nhỏ, dùng để sinh giá trị filter từ vị trí.

**2. Phần bảng so sánh explicit và implicit**

Với dòng explicit, ta lưu trực tiếp một vector `h[0...L-1]`. Cụm này đọc là: vector filter `h` gồm các phần tử từ `h0` đến `h_(L-1)`, tức là có khoảng `L` giá trị filter. Vì vậy nếu sequence length `L` tăng, filter cũng dài hơn và số tham số dễ tăng theo.

Với dòng implicit, ta không lưu từng giá trị filter riêng. Thay vào đó, mô hình học một hàm sinh `h_t` từ vị trí `t`. Vì tham số nằm trong FFN nhỏ, nên số tham số chính không tăng theo từng vị trí của filter.

Nếu cần nói ví dụ số, `4096` và `8192` ở đây là độ dài chuỗi, tức 4096 token hoặc 8192 token. Ý là: khi cần filter cho chuỗi dài 4096 hoặc 8192 token, Hyena có thể đưa các vị trí từ `0` đến `L-1` vào hàm sinh filter để tạo ra đủ giá trị, thay vì học riêng một tham số cho từng vị trí.

**3. Phần pipeline sinh filter**

Bắt đầu từ position `t`, tức vị trí hoặc khoảng cách đang cần sinh filter. Sau đó đưa `t` qua positional encoding để biến vị trí này thành biểu diễn mà mô hình hiểu được. Biểu diễn đó đi qua small FFN, đọc là mạng feed-forward nhỏ, để tạo ra raw filter value, tức giá trị filter ban đầu. Cuối cùng raw value được nhân với `Window(t)` để ra giá trị filter cuối cùng `h_t`.

**4. Phần window/decay**

`Window(t)` giúp kiểm soát filter ở các khoảng cách xa, tránh việc giá trị filter dao động quá mạnh và làm quá trình học kém ổn định.

Câu chốt là: Hyena học quy luật sinh filter, không học từng phần tử filter một cách explicit."

**Ghi chú phụ nếu bị hỏi FFN có phải FFT không:** Không. `FFN` là mạng feed-forward dùng để sinh filter ở slide 26. `FFT` là biến đổi Fourier nhanh dùng để tính convolution nhanh ở slide 27.

**Câu chuyển sang slide 27/38:**

"Sau khi đã sinh được filter dài, bước tiếp theo là tính convolution dài đó sao cho nhanh."

---

## Slide 27/38 - FFTConv

**Mục tiêu slide:** Giải thích vì sao convolution dài có thể rơi về `O(L log L)`.

**Lời thoại theo thứ tự trên slide:**

"Slide này giải thích vì sao long convolution của Hyena vẫn tính được nhanh.

**1. Phần ý tưởng chính**

Nếu tính convolution trực tiếp trong miền thời gian, tại mỗi vị trí output ta phải lấy một tổng dài của nhiều token quá khứ. Một output đã tốn nhiều phép nhân cộng; có `L` output thì chi phí gần bậc hai theo `L`.

Hyena dùng FFTConv để tránh cách tính trực tiếp này. `FFT` là Fast Fourier Transform, đọc là biến đổi Fourier nhanh.

Ý tưởng trong box là: thay vì tính convolution trực tiếp trong miền thời gian, ta chuyển signal và filter sang miền tần số. Trong miền tần số, phép convolution có thể được tính bằng phép nhân element-wise, tức nhân từng phần tử tương ứng. Sau đó dùng iFFT để đổi kết quả quay lại miền thời gian.

**2. Phần pipeline FFTConv**

Bước 1, lấy `FFT` của filter và `FFT` của signal. `FFT` đọc là "ép ép ti", viết tắt của Fast Fourier Transform, tiếng Việt là biến đổi Fourier nhanh. Signal ở đây là chuỗi hoặc trạng thái đang được convolution, ví dụ `z(n)` trong Hyena recurrence. Filter là `h(n)`. Sau bước FFT, cả signal và filter được chuyển từ miền thời gian sang miền tần số. Có thể hiểu đơn giản là ta đổi cách biểu diễn dữ liệu để convolution dễ tính hơn.

Bước 2, nhân hai kết quả FFT này element-wise trong frequency domain, tức miền tần số. Nghĩa là phần tử thứ nhất của FFT(signal) nhân với phần tử thứ nhất của FFT(filter), phần tử thứ hai nhân với phần tử thứ hai, và cứ như vậy. Đây là điểm giúp tính nhanh, vì thay vì trượt filter dài qua chuỗi, ta chỉ nhân từng cặp phần tử tương ứng trong miền tần số.

Bước 3, dùng biến đổi Fourier ngược, ký hiệu là `iFFT`, để chuyển kết quả từ miền tần số quay lại miền thời gian. `iFFT` đọc là "ai ép ép ti", nghĩa là inverse FFT. Output sau biến đổi Fourier ngược chính là kết quả convolution trên sequence, tức tín hiệu đã được trộn thông tin theo filter dài.

**3. Phần so sánh chi phí**

Direct convolution nghĩa là tính convolution trực tiếp bằng cách trượt filter dài qua toàn chuỗi. Cách này đắt khi filter rất dài, nên ít phù hợp với long-context.

FFTConv có chi phí khoảng `O(L log L)`. Ở đây `L` là độ dài chuỗi. Khi `L` lớn, `L log L` tăng chậm hơn nhiều so với `L^2`, nên FFTConv có lợi hơn cho context dài.

Nếu thầy hỏi chi tiết implementation, trong repo nhóm phần này nằm ở hàm `_causal_fft_conv` trong `models/hyena.py`. Hàm có zero-padding trước khi FFT để tránh circular convolution làm lẫn thông tin tương lai, rồi crop lại độ dài `L` để giữ causal convolution."

**Ghi chú phụ nếu thầy hỏi cơ sở toán:** Ý này dựa trên convolution theorem, tức định lý tích chập: convolution trong miền thời gian tương đương với nhân từng phần tử trong miền tần số. Slide không cần đọc công thức này, chỉ cần nói trực giác đổi miền để tính nhanh hơn.

**Câu chuyển sang slide 28/38:**

"Từ đó mình có thể chốt lại complexity và ý nghĩa thực tế của Hyena."

---

## Slide 28/38 - Complexity và Ý Nghĩa

**Mục tiêu slide:** Chốt lợi thế tính toán và nói rõ điều kiện lợi thế này phát huy.

**Lời thoại theo thứ tự trên slide:**

"Slide này chốt lại complexity theo sequence length.

**1. Phần bảng complexity**

Với Standard Attention, mỗi token phải so với rất nhiều token khác trong chuỗi. Vì vậy khi độ dài chuỗi là `L`, số cặp cần xử lý tăng theo `L^2`, và mô hình thường phải tạo một ma trận kích thước `L x L`.

FlashAttention vẫn có cùng bậc `O(L^2)` về số phép tính, nhưng nó sắp xếp cách tính thông minh hơn để giảm truy cập bộ nhớ. Vì vậy trong thực tế FlashAttention chạy nhanh và tiết kiệm bộ nhớ hơn attention thường, dù bản chất vẫn là attention.

Với Hyena, chi phí tính toán theo độ dài chuỗi là khoảng `O(N * L log L)`. Điểm quan trọng là Hyena không cần tạo ma trận attention.

**2. Phần công thức Hyena**

**Tên công thức complexity:** Sequence-length complexity - chi phí theo độ dài chuỗi.

**Cách đọc:** `O(N * L log L)` đọc là: chi phí tính toán của Hyena tăng cỡ `N` nhân `L log L` khi độ dài chuỗi tăng.

**Giải thích:** Big-O không phải số phép tính chính xác, mà là cách mô tả chi phí tăng nhanh thế nào khi `L` tăng. Trong công thức này, `L` là độ dài chuỗi, `log L` đến từ chi phí FFT, còn `N` là số bước recurrence hay order của Hyena. Dấu nhân nghĩa là nếu có `N` bước recurrence thì chi phí convolution nhanh được lặp khoảng `N` lần. Vì mỗi bước cần một convolution dài bằng FFT, nên chi phí theo `L` được ghi gọn là `O(N * L log L)`.

**Ý nghĩa:** Hyena khác attention ở chỗ không tạo attention matrix. Attention tăng theo `L^2`, còn Hyena tăng gần `L log L` theo chiều dài chuỗi, nên lợi thế rõ hơn khi `L` rất lớn.

**3. Phần dòng ghi chú về N và công thức đầy đủ của Hyena operator**

Trong Hyena, `N` là order hoặc số bước recurrence, thường được chọn nhỏ. Ví dụ repo nhóm dùng `order = 2`, tức mỗi block lặp hai bước convolution cộng gating.

Ngay dưới đó, slide có thêm công thức đầy đủ hơn cho **độ phức tạp tính toán của Hyena operator** trong paper: `O(N * D * L * (log L + D))`.

**Tên công thức:** Hyena operator compute complexity - độ phức tạp tính toán của Hyena operator.

**Cách đọc:** đọc là: chi phí tăng theo `N`, nhân với `D`, nhân với `L`, rồi nhân với phần trong ngoặc là `log L + D`.

**Giải thích:** Trong đó, `N` là số bước recurrence, `D` là model width, tức độ rộng biểu diễn của mô hình, và `L` là độ dài chuỗi. Trên bảng chính, mình rút gọn còn `O(N * L log L)` để nhấn vào điểm đang so sánh với attention: khi sequence length `L` tăng, Hyena tăng chậm hơn attention theo `L`.

**4. Phần box ý nghĩa**

Ý cần nhớ là: khi `L` rất lớn, `L log L` tăng chậm hơn `L^2`, nên lợi thế của Hyena rõ nhất ở long-context.

**5. Phần lưu ý cuối**

Cũng cần nói công bằng rằng Hyena không nhất thiết nhanh hơn ở `L` nhỏ vì FFT có overhead. Vì vậy slide này không nói Hyena luôn nhanh hơn, mà nói lợi thế rõ nhất khi context đủ dài."

**Câu chuyển sang slide 29/38:**

"Vậy paper gốc báo cáo kết quả thực nghiệm như thế nào?"

---

## Slide 29/38 - Kết Quả Paper Gốc

**Mục tiêu slide:** Tóm tắt kết quả đủ tự tin nhưng không lẫn với kết quả nhóm.

**Lời thoại theo thứ tự trên slide:**

"Slide này chỉ nói về kết quả của paper gốc, chưa phải kết quả reproduction của nhóm.

**1. Phần quality**

Phần quality đọc theo từng benchmark.

Với dataset WikiText-103, paper báo cáo Hyena-3 có chất lượng gần Transformer 125M. Kết quả này nằm ở **Table 7 trong Appendix A.2, trang PDF 16** của paper, phần perplexity trên WikiText-103. Ở đây `125M` đọc là 125 triệu tham số, tức quy mô mô hình.

Với dataset The Pile, paper báo cáo kết quả của Hyena-2 ở quy mô 335M. Kết quả này nằm ở **Table 3 trong Section 4.2 - Language Modeling, trang PDF 8**, phần perplexity trên The Pile. `335M` đọc là 335 triệu tham số. Ở đây chỉ cần nhấn vào ý chính: Hyena-2 cạnh tranh tốt ở cùng quy mô mô hình; mình không cần đi sâu vào mô hình baseline.

Với associative recall, paper cho thấy Hyena giữ chất lượng ở chuỗi rất dài, từ `30K` đến `131K` token, trong khi nhiều baseline bị `OOM`. Kết quả này nằm ở **Table 2 trong Section 4.1, trang PDF 8**, phần associative recall trên sequence dài. `OOM` là out of memory, tức không đủ bộ nhớ để chạy.

Ý của phần quality là: Hyena không chỉ nhắm tới tốc độ ở long-context, mà chất lượng cũng đủ cạnh tranh trong các benchmark paper báo cáo.

**2. Phần efficiency**

Phần efficiency đọc theo từng độ dài chuỗi.

Ở `2K`, tức khoảng 2 nghìn token, paper nói đây là gần vùng crossover. Crossover nghĩa là vùng bắt đầu chuyển từ attention có lợi hơn sang Hyena có lợi hơn.

Ở `8K`, tức khoảng 8 nghìn token, Hyena nhanh hơn khoảng 5 lần so với attention thường và khoảng 2 lần so với FlashAttention.

Ở `64K`, tức khoảng 64 nghìn token, paper báo cáo Hyena nhanh hơn khoảng 100 lần so với FlashAttention.

Các kết quả runtime này nằm ở **Figure 6 trong Section 4.4 - Benchmarking, trang PDF 9**. Figure 6 so sánh runtime của Hyena, Attention và FlashAttention theo nhiều sequence length khác nhau.

Một chi tiết quan trọng là điểm giao không xuất hiện ngay ở chuỗi ngắn. Paper nói Hyena bắt đầu vượt attention quanh 2048 token, và vượt FlashAttention khoảng 4096 đến 8192 token. Điều này khớp với slide trước: lợi thế của Hyena rõ nhất khi context đủ dài.

**3. Phần box kết luận**

Câu kết của slide này là: paper gốc báo cáo Hyena vừa thu hẹp khoảng cách chất lượng với Transformer, vừa có lợi thế tốc độ rõ ràng ở long-context. Sau phần này mới chuyển sang reproduction của nhóm ở quy mô nhỏ hơn."

**Câu chốt ngắn:**

"Tóm lại, kết quả gốc cho thấy Hyena không chỉ là ý tưởng lý thuyết; nó có chất lượng cạnh tranh và có lợi thế rõ khi sequence length lớn."

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

### Nếu bị hỏi: "Hyena khác attention ở điểm nào quan trọng nhất?"

Trả lời ngắn:

> Attention tạo ma trận `L x L` để so sánh các cặp token. Hyena không tạo ma trận đó, mà dùng long convolution để đưa thông tin xa về và dùng gating để chọn lọc theo input.

### Nếu bị hỏi: "Long convolution có phải giống attention không?"

Trả lời ngắn:

> Không giống hoàn toàn. Long convolution giúp token hiện tại nhận thông tin từ quá khứ xa, nhưng cách trộn có cấu trúc theo filter. Attention thì học trọng số giữa từng cặp token. Hyena dùng thêm gate để phép trộn phụ thuộc input hơn.

### Nếu bị hỏi: "Gating có phải chỉ là bật/tắt 0 và 1 không?"

Trả lời ngắn:

> Không. Gate là hệ số liên tục. Nó có thể giảm tín hiệu, giữ tín hiệu, hoặc cho tín hiệu đi qua mạnh hơn tùy input. Vì vậy nó giống bộ điều chỉnh cường độ hơn là công tắc bật tắt cứng.

### Nếu bị hỏi: "FFN và FFT khác nhau thế nào?"

Trả lời ngắn:

> `FFN` là mạng feed-forward nhỏ, dùng ở slide 26 để sinh filter từ vị trí. `FFT` là biến đổi Fourier nhanh, dùng ở slide 27 để tính convolution nhanh. Nói gọn: FFN sinh filter, FFT tính convolution.

### Nếu bị hỏi: "Vì sao implicit filter giúp ít tham số hơn?"

Trả lời ngắn:

> Vì mô hình không học riêng từng giá trị filter từ `h0` đến `h_(L-1)`. Nó học một hàm sinh filter: đưa vị trí `t` vào thì sinh ra `h_t`. Do đó khi chuỗi dài hơn, ta sinh thêm giá trị filter thay vì thêm một tham số riêng cho mỗi vị trí.

### Nếu bị hỏi: "Vì sao FFTConv nhanh hơn direct convolution?"

Trả lời ngắn:

> Direct convolution phải trượt filter dài qua toàn chuỗi nên rất tốn khi `L` lớn. FFTConv đổi signal và filter sang miền tần số, nhân từng phần tử, rồi dùng biến đổi Fourier ngược để quay lại sequence output. Nhờ vậy chi phí tăng khoảng `L log L` thay vì gần bậc hai theo `L`.

### Nếu bị hỏi: "Hyena có luôn nhanh hơn FlashAttention không?"

Trả lời ngắn:

> Không. Ở chuỗi ngắn, FFT có overhead nên Hyena chưa chắc nhanh hơn. Paper nhấn mạnh lợi thế của Hyena rõ nhất ở long-context, ví dụ vùng 8K token trở lên và đặc biệt 64K token.

### Nếu bị hỏi: "Các kết quả slide 29 lấy ở đâu trong paper?"

Trả lời ngắn:

> WikiText-103 nằm ở Table 7, Appendix A.2, trang PDF 16. The Pile nằm ở Table 3, Section 4.2, trang PDF 8. Associative recall nằm ở Table 2, Section 4.1, trang PDF 8. Runtime nằm ở Figure 6, Section 4.4, trang PDF 9.

### Nếu bị hỏi: "Kết quả slide 29 có phải nhóm mình reproduce không?"

Trả lời ngắn:

> Không. Slide 29 là kết quả paper gốc. Phần reproduction của nhóm nằm ở phần sau do Quang trình bày, với quy mô nhỏ hơn.

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
