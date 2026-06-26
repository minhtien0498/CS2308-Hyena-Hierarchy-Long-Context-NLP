# Speaker Notes

Nguồn: `tv2_slides_marp.md`

Tài liệu này được viết theo kiểu "script nói" để dễ tập thuyết trình. Bạn không cần đọc nguyên văn, nhưng có thể bám vào mạch ý của từng slide.

## Slide 1. Hyena Hierarchy

Ở phần này, mình mở đầu sau khi TV1 đã trình bày bài toán của self-attention, đặc biệt là chi phí `O(L^2)` khi sequence length `L` tăng lên. Từ đó, mục tiêu của TV2 là trả lời hai câu hỏi chính. Thứ nhất, nếu không dùng self-attention thì Hyena dùng toán tử nào để thay thế. Thứ hai, vì sao toán tử đó vẫn có thể mô hình hóa phụ thuộc xa nhưng lại scale tốt hơn khi context dài.

Bạn có thể mở bằng một câu rất tự nhiên như sau: "Ở phần trước, nhóm đã thấy attention rất mạnh nhưng bị nghẽn khi sequence dài. Bây giờ mình sẽ giới thiệu Hyena, một hướng thay thế attention bằng convolution dài kết hợp gating, và đây là ý tưởng chính giúp mở rộng long-context rẻ hơn."

Nếu muốn đặt kỳ vọng cho người nghe ngay từ đầu, có thể nói thêm: "Phần này không đi qua tất cả chi tiết toán học của paper, mà tập trung vào trực giác, cơ chế vận hành, và ý nghĩa về complexity."

## Slide 2. 1. Từ Attention Sang Hyena

Đây là slide chuyển ý quan trọng nhất giữa TV1 và TV2. Ở đây, mình nên nhấn mạnh rằng Hyena không phải là một bản xấp xỉ attention theo kiểu "làm attention nhanh hơn", mà là một operator khác hẳn, được thiết kế để giữ khả năng truyền thông tin xa và tính linh hoạt theo input.

Mạch nói gợi ý:

"Nếu nhìn vào bảng này, mình thấy attention có ba điểm mạnh. Thứ nhất, nó trộn thông tin trên toàn bộ chuỗi. Thứ hai, nó có tính chọn lọc theo nội dung input. Thứ ba, nó cho chất lượng language modeling rất tốt. Vấn đề là khi `L` dài, attention phải xử lý một ma trận `L x L`, nên time và memory đều tăng rất nhanh. Ý tưởng của Hyena là tách bài toán này thành ba mảnh thay thế: dùng long convolution để truyền thông tin xa, dùng data-controlled gating để giữ tính content-aware, và tính convolution bằng FFTConv để có chi phí gần `O(L log L)`."

Bạn cũng có thể chèn một câu để tránh hiểu nhầm:
"Vì vậy, cách nghĩ đúng ở đây không phải là 'Hyena có attention matrix nào ẩn bên trong', mà là 'Hyena thay cả cơ chế đó bằng một operator có cấu trúc khác'."

Nếu muốn phần mở của mình đậm hơn một chút, có thể chốt ngay ở slide này:
"Điểm đáng chú ý của bài báo không phải chỉ là giảm độ phức tạp, mà là họ dám thay attention bằng một toán tử mới mà vẫn giữ được mục tiêu language modeling."

Ghi chú phân công:
- Kiên có thể đóng vai trò nói phần bottleneck của attention.
- Tiến tiếp sang Hyena operator.
- Quang nói phần reproduction quy mô nhỏ ở TV3.

## Slide 3. 2. Ý Tưởng Chính Của Hyena

Đây là slide bản đồ của cả phần method. Mình không nên nói quá sâu từng ô trên slide, mà dùng nó để cho người nghe biết phần sau sẽ giải quyết từng ý như thế nào.

Một cách nói tự nhiên:
"Nếu tóm gọn Hyena trong một câu, thì Hyena = long convolution + data-controlled gating. Đầu vào sẽ được chiếu thành nhiều stream, trong đó có stream giá trị và các stream gate. Sau đó, mô hình lặp đi lặp lại một thao tác: lấy signal hiện tại, cho nó đi qua một long convolution, rồi dùng gate phụ thuộc input để giữ hoặc giảm từng phần thông tin. Cuối cùng, sau nhiều bước như vậy, ta thu được output."

Nói tiếp để mở đường cho các slide sau:
"Từ slide này trở đi, mình sẽ tách ra thành 5 câu hỏi nhỏ: long convolution là gì, gating có vai trò gì, recurrence được viết như thế nào, vì sao filter dài không làm nổ tham số, và vì sao có thể tính nhanh bằng FFT."

Nếu thấy người nghe bắt đầu mất mạch, có thể thêm một câu rất đời thường:
"Cụ thể hơn, có thể hiểu convolution phụ trách 'mang thông tin xa về', còn gating phụ trách 'quyết định có nên giữ thông tin đó hay không'."

## Slide 4. 3. Long Convolution

Đây là slide để tạo trực giác rằng Hyena vẫn có thể nhìn xa mà không cần attention matrix dày đặc. Điểm cần nhấn mạnh là sự khác nhau giữa convolution ngắn trong CNN thường và long convolution trong Hyena.

Script gợi ý:
"Trong CNN thông thường, kernel rất ngắn, ví dụ chỉ nhìn vài token lân cận. Như vậy, mô hình xử lý tốt local pattern nhưng khó nhớ được quan hệ rất xa nếu không xếp rất nhiều tầng. Còn trong Hyena, filter có độ dài gần bằng sequence, nên một token ở vị trí `t` có thể nhận ảnh hưởng từ rất nhiều token trước đó, thực chất là từ toàn bộ phần lịch sử cần thiết."

Khi chỉ vào công thức, không cần đọc ký hiệu quá máy móc. Có thể nói:
"Công thức này nói rằng output tại thời điểm `t` là tổng có trọng số của các token trước đó. Mỗi token trong quá khứ đóng góp một lượng nào đó, và mức đóng góp đó được điều khiển bởi filter `h`."

Sau đó chốt ý nghĩa:
"Vì đây là causal convolution, nên nó chỉ nhìn về quá khứ, phù hợp với language modeling. Như vậy, Hyena vẫn có cách để kết nối thông tin xa, nhưng không cần xây một ma trận attention `L x L` cho mọi cặp token."

Nếu muốn để người nghe dễ hình dung hơn:
"Có thể tưởng tượng self-attention là mỗi token tự đi hỏi từng token khác xem có liên quan không. Còn long convolution thì giống như có sẵn một bộ mẫu để quét qua lịch sử và tổng hợp lại một cách có cấu trúc."

## Slide 5. 4. Data-Controlled Gating

Sau khi nói về convolution, slide này trả lời câu hỏi quan trọng nhất: nếu chỉ dùng convolution thì có bị quá tĩnh và thiếu linh hoạt không. Câu trả lời của Hyena là có gating phụ thuộc input.

Mạch nói gợi ý:
"Nếu chỉ dùng convolution thuần túy, thì vấn đề là cùng một filter sẽ áp dụng cho mọi input, trong khi language modeling cần khả năng chọn lọc theo ngữ cảnh. Cùng là một token, nhưng trong câu này nó có thể quan trọng, sang câu khác thì không. Vì vậy Hyena thêm một cơ chế gating."

Chỉ vào ví dụ số trên slide:
"Ở đây, conv output có thể xem là thông tin đã được mang về từ xa. Nhưng gate mới quyết định phần nào được giữ mạnh, phần nào bị giảm. Gate lớn thì thông tin được truyền qua nhiều hơn, gate nhỏ thì bị làm yếu đi. Như vậy, Hyena không chỉ tổng hợp thông tin xa, mà còn làm điều đó theo cách phụ thuộc vào input hiện tại."

Câu chốt nên nói rõ:
"Đây là lý do paper dùng cụm từ 'data-controlled'. Filter có cấu trúc để tính hiệu quả, nhưng khả năng chọn lọc lại vẫn do dữ liệu đầu vào điều khiển."

Nếu thầy hỏi "gate có phải 0/1 không", bạn có thể trả lời:
"Không. Gate là một tín hiệu liên tục học được, nên nó mềm và linh hoạt hơn rất nhiều so với một công tắc bật/tắt đơn giản."

## Slide 6. 5. Hyena Recurrence

Đây là slide trọng tâm nhất của phần TV2, vì nó viết ra công thức cốt lõi của operator. Ở slide này, tốc độ nói nên chậm hơn một chút và giải thích lần lượt từng biến.

Script gợi ý:
"Công thức trung tâm của Hyena là `z^{n+1}_t = x^n_t * (h^n * z^n)_t`. Mình đọc nó theo trực giác như sau. Đầu tiên, `z^n` là signal hiện tại ở bước `n`. Signal này được đưa qua một long convolution với filter `h^n`, nghĩa là ta tổng hợp thông tin từ lịch sử. Sau đó, kết quả tại vị trí `t` được nhân với gate `x^n_t`, là gate sinh ra từ input. Kết quả sau cùng trở thành `z^{n+1}` để đưa sang bước tiếp theo."

Nói rõ ý nghĩa từng thành phần:
- "`z^1 = v`" là value stream ban đầu.
- "`h^n`" là filter ở bước thứ `n`.
- "`x^n_t`" là gate tại token `t`.
- "`N`" là số lần lặp, hay còn gọi là order của Hyena.

Sau đó chốt mạch vận hành:
"Như vậy, mỗi bước của Hyena đều có hai thao tác nối tiếp nhau: convolution để trộn thông tin có cấu trúc, rồi gating để chọn lọc theo input. Lặp lại nhiều bước như vậy sẽ tạo ra một operator mạnh hơn một convolution đơn lẻ."

Nếu bị hỏi Hyena khác CNN ở đâu, có thể nói:
"CNN thường là xếp các lớp convolution. Còn Hyena xen kẽ long convolution và gate phụ thuộc input ở nhiều bước, nên mức độ data-control rõ hơn. Đây là điểm giúp nó gần hơn với nhu cầu language modeling."

## Slide 7. 6. Order-N Hierarchy

Slide này giải thích vì sao tên paper có chữ "Hierarchy". Mình không cần đi qua các liên hệ lịch sử như H3 hay GSS quá kỹ, chỉ cần giữ một trực giác rõ ràng về việc lặp nhiều tầng tương tác.

Một cách nói đơn giản:
"Hyena không nhất thiết chỉ có một bước convolution rồi xong. Nó có thể lặp nhiều bước convolution + gating. Mỗi lần lặp như vậy thêm một tầng xử lý có cấu trúc, nên paper gọi đây là hierarchy. Khi `N` tăng, operator có khả năng biểu diễn phong phú hơn."

Sau đó nói theo đúng repo nhóm:
"Trong reproduction của nhóm, để bài toán gọn và dễ chạy ổn định hơn, mình dùng cấu hình nhỏ với `order = 2`. Tức là mình lặp hai lần theo mạch conv rồi gate."

Nếu muốn nói mềm hơn:
"Bạn có thể hiểu order như số tầng xử lý nội bộ của operator. Order cao hơn thì mạnh hơn, nhưng đồng thời phức tạp hơn và tốn tài nguyên hơn."

## Slide 8. 7. Matrix View

Đây là slide để tạo trực giác toán học, chứ không phải để chứng minh. Mục tiêu là giúp người nghe thấy vì sao Hyena vẫn phụ thuộc input, nhưng không cần một attention matrix dense.

Script gợi ý:
"Nếu viết dưới dạng ma trận, gating `x^n` có thể xem là một diagonal matrix `D_x`, vì nó chỉ nhân theo từng vị trí. Còn convolution có thể xem là một Toeplitz matrix `S_h`, vì đó là cách viết ma trận của một phép conv 1D. Khi đó, Hyena có dạng xen kẽ `D_x` và `S_h`."

Chỉ vào dòng text trên slide:
"Điểm khác biệt lớn là attention tạo ra một ma trận dense `A(x)` kích thước `L x L`, còn Hyena thay nó bằng một chuỗi các phép nhân có cấu trúc. `D_x` rẻ vì là diagonal, `S_h` rẻ hơn vì có thể tính bằng FFT. Nhưng do vẫn có `D_x`, operator này vẫn phụ thuộc input, chứ không phải một conv cố định."

Nếu thấy người nghe bị ngợp, chỉ cần chốt một câu:
"Thông điệp chính của slide này là: Hyena vẫn content-aware, nhưng dùng cấu trúc ma trận đặc biệt để tính rẻ hơn attention."

## Slide 9. 8. Implicit Filter

Slide này giải thích một điểm rất hay của paper: filter dài nhưng không cần học trực tiếp hàng nghìn hay hàng chục nghìn tham số cho từng vị trí.

Mạch nói gợi ý:
"Nếu học filter theo cách explicit, nghĩa là lưu thẳng `h[0], h[1], ..., h[L-1]`, thì sequence càng dài, filter càng dài, và tham số sẽ tăng theo `L`. Paper tránh điều đó bằng cách học một hàm sinh filter."

Nói tiếp theo công thức:
"Cụ thể, tại mỗi vị trí `t`, mô hình đưa positional encoding của `t` qua một FFN nhỏ để sinh ra giá trị filter `h_t`. Sau đó, một hàm window hoặc decay được nhân vào để giúp filter ổn định hơn, đặc biệt ở khoảng cách xa."

Ẩn dụ để dễ nói:
"Có thể hiểu nó như việc không học từng điểm của đường cong, mà học một công thức để vẽ ra cả đường cong đó."

Chốt ý:
"Nhờ vậy, Hyena có thể có filter rất dài phù hợp với long-context, nhưng số tham số không cần nổ theo độ dài chuỗi."

## Slide 10. 9. FFTConv

Đây là slide nói về hiện thực hiệu quả. Ở đây, mình nên tránh lao vào lý thuyết Fourier quá sâu. Điều quan trọng là người nghe hiểu ý tưởng đổi miền để biến convolution thành phép nhân để tính nhanh hơn.

Script gợi ý:
"Long convolution nghe hợp lý về mặt ý tưởng, nhưng nếu tính trực tiếp thì vẫn tốn kém khi filter rất dài. Vì vậy Hyena dùng FFT convolution. Ý tưởng là đưa filter và signal sang miền tần số, khi đó phép convolution trong miền thời gian trở thành phép nhân element-wise trong miền tần số. Sau khi nhân xong, ta dùng inverse FFT để quay về lại output trên sequence."

Bạn có thể đi qua 3 bước trên slide:
"Bước 1 là FFT của `h` và `u`. Bước 2 là nhân từng phần tử trong miền tần số. Bước 3 là iFFT để lấy output trở lại. Chính nhờ cấu trúc này mà chi phí giảm xuống gần `O(L log L)`."

Nếu muốn gắn với code:
"Trong repo, logic này nằm trong `HyenaOperator._causal_fft_conv`. Ở mức code, mình sẽ thấy `rfft`, nhân `H * V`, rồi `irfft` và cắt về độ dài `L` cần thiết."

Nếu bị hỏi "tại sao không luôn nhanh hơn attention", có thể nói trước:
"FFT có overhead, nên với sequence ngắn thì lợi thế chưa chắc lộ rõ. Điểm mạnh của nó nằm ở context dài."

## Slide 11. 10. Complexity Và Ý Nghĩa

Đây là slide để kết nối method với lý do tại sao paper quan tâm đến Hyena cho bài toán long-context. Ở đây, mình nên nói cân bằng: không thần thánh hóa Hyena, nhưng cũng phải làm rõ điểm mạnh thực sự của nó.

Mạch nói gợi ý:
"Nếu so sánh ở mức complexity, standard attention có time và memory `O(L^2)`. FlashAttention cải thiện cách truy cập memory và tối ưu thực thi rất giỏi, nhưng về mặt compute bản chất vẫn là `O(L^2)`. Còn Hyena có độ phức tạp xấp xỉ `O(N * L log L)`, trong đó `N` là order. Vì vậy, khi `L` tăng rất lớn, tốc độ tăng của Hyena chậm hơn attention."

Sau đó có thể đưa ví dụ trực giác:
"Ví dụ nếu `L = 1K`, thì `L^2` đã vào khoảng một triệu, còn `L log L` chỉ ở mức hàng chục nghìn. Khi lên `8K` hay `64K`, khoảng cách này càng rõ hơn. Do đó, paper không nói Hyena luôn nhanh hơn trong mọi tình huống, mà nói rằng nó có điểm rơi rất tốt khi context dài."

Câu cần nhấn mạnh:
"Nói cách khác, Hyena là một thiết kế có lợi về scaling. Ở sequence ngắn, overhead FFT và implementation có thể làm nó chưa vượt trội. Nhưng khi độ dài chuỗi tăng lên, lợi thế complexity mới bắt đầu thể hiện rõ."

Nếu muốn nối sang ý "vì sao paper này hay", bạn có thể thêm:
"Theo em, chỗ đáng giá là paper không chỉ nói về tốc độ, mà còn cố thu hẹp quality gap với Transformer. Tức là họ không đánh đổi hoàn toàn chất lượng để lấy scaling."

## Slide 12. 11. Kết Quả Paper Gốc

Đây là slide tổng hợp xem paper gốc đã chứng minh được gì. Rất quan trọng là tách bạch giữa kết quả của paper và kết quả reproduction của nhóm.

Script gợi ý:
"Đến đây, mình đã trình bày cơ chế. Câu hỏi tiếp theo là: paper gốc có chứng minh được gì không? Câu trả lời là có, trên hai mặt. Về quality, Hyena đạt kết quả gần với Transformer trên các benchmark language modeling như WikiText-103 và The Pile, đồng thời làm tốt trên một số bài synthetic có yêu cầu phụ thuộc dài. Về efficiency, khi sequence length tăng, Hyena cho thấy lợi thế runtime rõ ràng hơn attention, và trong paper thì ở mức 64K, tác giả báo cáo speedup rất lớn."

Nếu thầy hỏi "bài này có gì hay mà được đăng", bạn có thể nối ngay từ slide này:
"Theo em, cái hay của bài không chỉ nằm ở việc chạy nhanh hơn, mà ở chỗ họ đề xuất một operator mới thay attention, chứ không chỉ sửa attention cũ. Họ kết hợp long convolution, data-controlled gating và implicit filter thành một kiến trúc attention-free vẫn đủ mạnh cho language modeling. Vì vậy bài có cả ý tưởng mới, lý do lý thuyết rõ, và kết quả thực nghiệm đủ thuyết phục."

Sau đó phải nhấn rõ giới hạn:
"Tuy nhiên, đây là kết quả của paper gốc ở quy mô lớn, implementation và benchmark cũng mạnh hơn rất nhiều so với bài tập môn học của nhóm. Vì vậy mình không nên đồng nhất phần này với reproduction của nhóm."

Câu chuyển tiếp rất hợp:
"Từ đây, TV3 sẽ chuyển sang phần reproduction quy mô nhỏ để xem trong điều kiện đơn giản hơn, nhóm có quan sát được xu hướng cốt lõi tương tự hay không."

## Slide 13. Chuyển Sang Reproduction

Nếu giữ slide này, nó đóng vai trò câu nối rất đẹp giữa TV2 và TV3.

Bạn có thể nói:
"Tất cả các kết quả ở slide trước là của paper gốc ở quy mô lớn. Còn trong phạm vi môn học, nhóm không nhằm tái hiện toàn bộ benchmark đó, mà thu nhỏ bài toán lại: model nhỏ hơn, sequence ngắn hơn, benchmark gọn hơn. Mục tiêu của reproduction không phải là đạt đúng từng con số của paper, mà là kiểm tra xem xu hướng chính có còn giữ được hay không. Sau đây, Quang sẽ trình bày phần reproduction của nhóm."

Nếu bỏ slide này khỏi deck, ý trên vẫn có thể nói như câu kết của slide 12.
