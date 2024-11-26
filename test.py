# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

for i in range(1, 5):
    file_path = f"preprocessed_data\\preprocessed_{i}.csv"  
    data = pd.read_csv(file_path)
   
    with open("preprocessed_data\\preprocessed_all.csv", 'a', encoding='utf-8') as f:
        data.to_csv(f, header=f.tell()==0, index=False)
        
print("Gộp các file thành công vào preprocessed_all.csv")



file_path = "preprocessed_data\\preprocessed_all.csv"  # Đường dẫn đến file dữ liệu của bạn
data = pd.read_csv(file_path)

# Kết hợp các cột văn bản (Title, Description, Content)
data['combined_text'] = data['Title'] + " " + data['Description'] + " " + data['Content']

# Loại bỏ các dòng có giá trị NaN trong cột 'combined_text'
data = data.dropna(subset=['combined_text']) 

# Kiểm tra số lượng mẫu của mỗi lớp
category_counts = data['Category'].value_counts()

# Loại bỏ các lớp có ít hơn 2 mẫu
valid_classes = category_counts[category_counts >= 2].index
data_filtered = data[data['Category'].isin(valid_classes)]

# Mã hóa nhãn Category thành số
label_encoder = LabelEncoder()
data_filtered['Category_encoded'] = label_encoder.fit_transform(data_filtered['Category'])

# Tách dữ liệu thành các biến đầu vào và nhãn
X = data_filtered['combined_text']
y = data_filtered['Category_encoded']

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Biến đổi văn bản thành vector TF-IDF
tfidf_vectorizer = TfidfVectorizer(max_features=5000)  # Không sử dụng stop_words vì dữ liệu đã được làm sạch
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)

# Xây dựng mô hình mạng nơ-ron
num_classes = len(label_encoder.classes_)
model = Sequential([
    Dense(128, input_shape=(5000,), activation='relu'),
    Dropout(0.3),
    Dense(64, activation='relu'),
    Dropout(0.3),
    Dense(num_classes, activation='softmax')
])

# Biên dịch mô hình
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Huấn luyện mô hình
history = model.fit(X_train_tfidf.toarray(), y_train, 
                    validation_data=(X_test_tfidf.toarray(), y_test), 
                    epochs=200, batch_size=16, verbose=1)

# Đánh giá mô hình
test_loss, test_accuracy = model.evaluate(X_test_tfidf.toarray(), y_test, verbose=0)
print(f"Test Accuracy: {test_accuracy * 100:.2f}%")


new_text = """

Cũng như tất cả mọi người dân trên lãnh thổ quốc gia và trên thế giới, các nhà lãnh đạo của Trung Quốc hẳn cũng đang dõi theo kết quả của chiến dịch tranh cử khốc liệt đang diễn ra tại Hợp chủng quốc Hoa Kỳ và đang bồn chồn băn khoăn không biết kết quả sẽ có tác động như thế nào đến họ. Sau bốn năm trời kèn cựa với Donald Trump, dân Trung chắc nên đếm từng tháng, từng tuần, từng ngày hay từng phút cho đến cuộc bầu cử vào tháng 11, hy vọng rằng ứng viên Dân chủ mềm dẻo hơn sẽ tiếp quản Nhà Trắng, đúng chứ? Đó chắc chắn là điều mà Trump tin. Người Trung Quốc, ông tweet, “đang tuyệt vọng mong Sleepy Joe Biden đắc cử để họ có thể tiếp tục lừa dối nước Mĩ, như họ đã làm hàng thập kỉ trước, cho tới khi tôi xuất hiện!”
Điều này chưa chắc đã đúng. Theo quan điểm của Bắc Kinh thì, trong khi một tổng thống đảng Dân chủ có thể tái thiết lập chính sách ngoại giao dễ đoán hơn của Hoa Kì, nó vẫn có thể không có lợi cho Trung Quốc. Trên thực tế, Trump tái đắc cử thêm 4 năm nữa – dù có vẻ sẽ đi kèm với phiền toái và tranh cãi – có khi lại là một cơ hội béo bở cho Trung Quốc mở rộng phạm vi ảnh hưởng tại Đông Á và trên thế giới.
Tất nhiên là chúng ta không thể biết chắc chắn những nhân vật cấp cao của Trung Quốc muốn kết quả nào hơn, hoặc thậm chí liệu họ có cùng quan điểm với nhau hay không. Không một ứng viên nào nên trông đợi một lời tán dương thì Nhân Dân Nhật báo. Tuy nhiên, vẫn có những manh mối. Trong một bình luận cực kì khác thường, cựu đàm phán viên về mậu dịch của Trung Quốc Long Yongtu đã nói tại Hội nghị Thâm Quyến cuối năm ngoái: “Chúng tôi muốn Trump đắc cử; chúng tôi muốn chứng kiến điều đó xảy ra”. Những dòng tweet của ngài Tổng thống khiến cho ông ta trở nên “dễ đoán”, Long nói, và vì thế “là lựa chọn tốt nhất về đối thủ trong những cuộc đàm phán”. Vào tháng Năm, Hu Xijin, Tổng biên tập Thời báo Hoàn Cầu, cơ quan ngôn luận chính thức của Đảng Cộng sản Trung Quốc, đã tweet Trump rằng người Trung Quốc “mong rằng ông sẽ tái đắc cử bởi ông có thể khiến nước Mĩ trở nên quái gở và đáng ghét trong con mắt của thế giới. Ông thúc đẩy sự đoàn kết ở Trung Quốc”. Hu còn viết thêm “người dân Trung Quốc gọi ông là ‘Jianguo’, có nghĩa là “giúp dựng xây Trung Quốc.’” Long và Hu có thể không đại diện cho lãnh đạo Trung Quốc, nhưng không một nhân viên chính phủ hay nhân vật truyền thông đại chúng của Trung Quốc nào dám liều lĩnh ra những tuyên bố này một cách công khai nếu quan điểm của họ là một điều cấm kỵ đối với tầng lớp chính trị.
Vậy chuyện gì đang xảy ra? Rất nhiều người Mĩ tin (một cách sai lầm) rằng Trump là tổng thống đầu tiên dám đứng lên chống lại Trung Quốc. Xét cho cùng thì chính quyền của ông ta đã đánh thuế lên những mặt hàng xuất khẩu của Trung Quốc, trừng phạt một vài trong số những doanh nghiệp cũng như nhân viên chính phủ quan trọng nhất của họ, và gây sức ép bắt Trung Quốc phải giao dịch một cách công bằng – và dân Trung Quốc còn muốn nữa á? Tất nhiên là Trung Quốc sẽ muốn tránh một vụ tranh chấp thương mại đắt đỏ với một trong những bạn hàng lớn nhất của mình. Nhưng có thể Trump không đến nỗi ghê gớm trong mắt những nhân vật cấp cao của Trung Quốc như chúng ta vẫn nghĩ.
“Ông ta có một vài cảm tính mà Trung Quốc không thích, nhưng cũng không hoàn toàn bận tâm”, Minxin Pei, một chuyên gia về chính trị Trung Quốc tại Đại học Claremont McKenna, nói với tôi như vậy. “Ông ta không thực sự xem Trung Quốc là một đối thủ ý thức hệ. Trump hoàn toàn có thể bị thuyết phục nếu được giá”.
Đối với Trung Quốc, thì đây chính là chìa khóa. Cho dù Trump có đôi khi có những phản ứng liên quan đến những vấn đề chính trị hoặc nhân quyền mà Bắc Kinh cho là nhạy cảm – như là gần đây nhất, kí một sắc lệnh trừng phạt chính phủ Trung Quốc vì hành vi ngược đãi dân tộc thiểu số Duy Ngô Nhĩ – cá nhân ông ta thường tỏ ra không hứng thú, thậm chí tùy tiện. Trong cuốn sách mới xuất bản, cựu Cố vấn An ninh quốc gia John Bolton viết rằng Trump nói với Chủ tịch Trung Quốc Tập Cận Bình tại một bữa tối ở Osaka rằng những trại tập trung mà Bắc Kinh đang xây dựng để kiểm soát cộng đồng Duy Ngô Nhĩ là điều đúng đắn. Gần đây Trump cũng thừa nhận rằng ông ta đã trì hoãn việc trừng phạt những nhân viên chính phủ có liên quan đến những trại tập trung này để “bôi trơn” cho cuộc đàm phán liên quan đến một giao dịch thương mại của ông ta với Trung Quốc.
Trump cũng đã cho thấy sự mâu thuẫn về tư tưởng tương tự đối với sự đàn áp thẳng tay và quyết liệt của Bắc Kinh đối với những cuộc biểu tình ủng hộ dân chủ tại Hong Kong. Ngài tổng thống đã hứa hẹn những hình phạt cứng rắn để đáp trả hành động của Bắc Kinh – áp luật an ninh quốc gia lên Hong Kong nhằm những thành phần chống đối còn sót lại – và Ngoại trưởng Mike Pompeo đã ra những tuyên bố có tính hiếu chiến và đe dọa liên quan đến hành động này. Nhưng sự cam kết của Trump đối với vấn đề Hong Kong đôi khi có vẻ thờ ơ. Năm ngoái, trong khi hàng triệu người tuần hành trong thành phố, ông ta đã lảng tránh việc ủng hộ họ, và vào một thời điểm thậm chí đã nhắc lại lập trường của Đảng Cộng sản bằng việc gọi những cuộc biểu tình là “bạo loạn” và nói rằng đây hoàn toàn là vấn đề của Trung Quốc. “Điều đó là vấn đề giữa Hong Kong và Trung Quốc, bởi Hong Kong là một phần của Trung Quốc”, ông ta nói vào tháng Tám năm ngoái.
Thậm chí về mặt thương mại – một đề tài thường hay xuất hiện trong những tweet của ông ta – Trump vẫn chứng tỏ sự thiếu quyết tâm. Những đàm phán viên của Trung Quốc đã khéo léo thuyết phục ông ta đẩy những cuộc tranh luận về những vấn đề nguy cấp đối với nền kinh tế Hoa Kì – ví dụ những chương trình chính phủ trợ cấp cho các công ty từ Trung Quốc – xuống “giai đoạn hai” của công cuộc đàm phán, thứ đang dần trở thành hiện thực. Thay vào đó, Trump chấp nhận một thỏa thuận “giai đoạn một” eo hẹp hơn, được kí vào tháng Một, thứ chủ yếu tập trung vào việc Trung Quốc nhập thêm nông sản của Hoa Kì, nhưng lại có rất ít thay đổi về những hoạt động có tính phân biệt đối xử của Bắc Kinh.
Trump thậm chí còn làm ít hơn thế để kiềm chế sự vươn lên của Trung Quốc trên trường quốc tế. Thái độ khinh thị mà chính quyền Trump dành cho những tổ chức quốc tế đã giúp gia tăng sự ảnh hưởng Trung Quốc đối với họ – đáng chú ý nhất là tuyên bố rút khỏi Tổ chức Y tế Thế giới gần đây của ông ta. Trong khi Pompeo vẫn luôn phê phán chính sách của Tập, Sáng kiến xây dựng cơ sở hạ tầng Vành đai Con đường, là một cái bẫy nguy hiểm để gài những quốc gia nghèo khó, chính quyền của ông ta vẫn chưa đưa ra được một giải pháp thay thế. Trump đã tranh cãi một cách gay gắt về yêu sách đối với gần như toàn bộ vùng Biển Đông gây tranh cãi của Bắc Kinh bằng việc tăng sự hiện diện về mặt quân sự trên những vùng biển tranh chấp để giữ gìn tự do hàng hải, nhưng ông ta vẫn chưa tiếp nối hành động đó bằng bất kì chính sách ngoại giao nhất quán nào đối với Đông Nam Á, và ông ta vẫn lờ vấn đề này đi.
“Giới lãnh đạo Trung Quốc khá tự tin rằng dù cho họ có không chiếm được Biển Đông thì họ cũng vẫn đang thắng”, Gregory Poling, giám đốc Sáng kiến Minh bạch Hàng hải châu Á thuộc Trung tâm Nghiên cứu Chiến lược và Quốc tế tại Washington, nói với tôi. Để chống lại việc này sẽ cần sự nỗ lực của cả thế giới dẫn đầu bởi Mĩ, nhưng “bạn có thể chắc chắn rằng nó sẽ không xảy ra khi Trump còn tại vị”, Poling nói.
Đây là lí do chính tại sao Bắc Kinh có thể sẽ không phản đối một nhiệm kì nữa của Trump: Phong cách đối ngoại của ông ta – đơn phương, cá nhân hóa, và luôn gắn liền với những chủ đề về dollar-và-cents – đã làm hệ thống đồng minh truyền thống của Hoa Kì trở nên suy yếu. Trong khi Tổng thống Barack Obama có chính sách xoay trục châu Á, Trump chỉ thỉnh thoảng mới cho thấy hứng thú đối với khu vực, đặc biệt là thương mại và sự chim chuột giữa ông ta và nhà lãnh đạo Bắc Triều Tiên Kim Jong Un. Bắc Kinh chắc chắn đã để ý thấy mối quan hệ căng thẳng với hai đồng minh thân cận nhất của Mĩ tại khu vực – Hàn Quốc và Nhật Bản – bởi sự cố chấp và những vụ cãi nhau nhỏ mọn của ông ta về vấn đề thương mại và chi phí dành cho những căn cứ quân sự của Hoa Kỳ tại hai nước này.
Điều này hoàn toàn ổn đối với Bắc Kinh. Trong khi Mĩ lùi bước về sau, thì Trung Quốc tiến lên phía trước. Bắc Kinh đã và đang càng ngày trở nên quyết đoán trong khoảng thời gian Trump làm tổng thống. Bộ máy tuyên truyền của Trung Quốc đang lợi dụng phản ứng tồi tệ của Trump đối với đại dịch để chế giễu tổng thống và nền dân chủ Mĩ, làm dậy lên những ngờ vực về khả năng lãnh đạo thế giới của Hoa Kì, và miêu tả Trung Quốc như là một cường quốc có trách nhiệm hơn. Hu của Thời báo Hoàn Cầu đang cực kì vui sướng khi Trump vật lộn, hàng ngày anh ta xả từ con đập ngôn từ những dòng chữ chế giễu. “Ông hoàn toàn không biết kiểm soát đại dịch”, anh ta tweet về Trump vào tháng Sáu. “Nếu nước Mĩ cau có là một con người ngoài đời, thì người đó hẳn sẽ rất bẩn thỉu dơ dáy”. Anh ta còn tuyên bố, “Washington thực sự ngu ngốc”. Chính quyền Trung Quốc, bằng kĩ năng diệt virus thượng thừa, “củng cố lòng tin của quốc tế vào việc chiến thắng virus”, Liu Xiaoming, Đại sứ Trung Quốc tại Anh nói. (Dù không rõ tác động hữu hình của bình luận này đối với quan điểm của công chúng toàn thế giới, rất nhiều nhà ngoại giao cũng như quan chức Trung Quốc cho rằng nó hiệu quả).
Đứng trên lập trường của Trung Quốc, thì Trump không hề cứng rắn hơn mà ông ta chỉ khác biệt. Các tổng thống tiền nhiệm đã cố gắng gây áp lực với Trung Quốc trong khuôn khổ các quy tắc quốc tế hiện hành; còn Trump thì thích hành động bên ngoài hệ thống đó. Ví dụ, những người tiền nhiệm của ông ta đã lên án các hành vi thương mai không công bằng của Trung Quốc tại Tổ chức Thương mại Thế giới, gửi 21 đơn khiếu nại từ năm 2004 đến đầu năm 2017 (với tỉ lệ thành công khá cao). Chính quyền Trump công khai chê bai WTO, chỉ gửi 2 khiếu nại, một trong số đó là phản ứng trước sự trả đũa của Trung Quốc đối với chính sách thuế quan do chính Trump đưa ra. Trong khi các tổng thống tiền nhiệm đã tìm cách lấy lòng các cường quốc khác, đặc biệt là ở châu Âu và Đông Á, cũng có lợi ích trong việc buộc Trung Quốc phải chơi theo luật, thì Nhà Trắng hiện tại lại xa lánh Liên minh Châu Âu bằng cách đe dọa áp thuế cao, chỉ trích NATO, và đưa ra những công kích cá nhân nhằm vào những nhà lãnh đạo có ảnh hưởng nhất của phương Tây. Trong khi đó, tại châu Á, ông ta rút khỏi Hiệp định Đối tác Xuyên Thái Bình Dương, một hiệp ước nhằm củng cố quan hệ của Mĩ đối với các đồng minh.
Theo lẽ đó, một tổng thống Mĩ có chính sách đối ngoại “bình thường” hơn – trong đó Washington hợp tác chặt chẽ với đồng minh và ủng hộ các chuẩn mực và thể chế quốc tế - là không tốt cho Trung Quốc. Ứng cử viên của Đảng Dân chủ Joe Biden đã tuyên bố sẽ thành lập một liên minh các nước để cô lập và đối đầu với Trung Quốc. “Khi chúng ta hợp tác với những nền dân chủ khác, sức mạnh của chúng ta sẽ tăng gấp đôi”, Biden lập luận. “Trung Quốc không thể lờ đi hơn một nửa kinh tế toàn cầu”. Đó, chứ không phải Trump, mới là cơn ác mộng của Trung Quốc.
Dù ai thắng trong tháng 11 đi chăng nữa, chính sách đối với Trung Quốc không có khả năng trở nên mềm mỏng. Lưỡng đảng tại Washington đều đồng thuận rằng Trung Quốc là một mối đe dọa chiến lược đối với Hoa Kì, và không có cách nào để quay đồng hồ ngược trở lại những tháng ngày êm ả trước đây khi mà Mĩ còn kiên nhẫn trong việc can thiệp. “Số lượng người theo chủ trương mềm mỏng không còn nhiều nữa, kể cả bên cánh tả”, Poling nói. “Khi nhắc tới Trung Quốc, một Đảng viên Dân chủ hiện tại không còn là một Đảng viên Dân chủ thời Obama nữa. Điều đó về mặt chính trị không còn khả thi nữa”.
Pei từ Đại học Clarance McKenna dự đoán một vài người ở Bắc Kinh có thể vẫn thích Biden chiến thắng hơn, với hy vọng tạm dừng căng thẳng trong khi Đảng Dân chủ, ít nhất là trong thời gian đầu, tập trung vào những vấn đề quốc nội. Nhưng người Trung Quốc có thể sẽ hối tiếc, ông nói. “Những người ủng hộ Trump tin rằng chỉ có Hoa Kì mới có thể giáng cho Trung Quốc một đòn chí mạng”, Pei nói. “Đảng Dân chủ có thể sẽ liên hệ với các đồng minh để thành lập một mặt trận thống nhất hơn nhiều để chống lại Trung Quốc. Nếu Đảng Dân chủ thành công, thì về lâu dài Trung Quốc sẽ khó khăn hơn nhiều”."  
"""
# Biến đổi đoạn văn bản mới thành vector TF-IDF
new_text_tfidf = tfidf_vectorizer.transform([new_text])

# Dự đoán nhãn (category) cho đoạn văn bản mới
predicted_category_encoded = model.predict(new_text_tfidf.toarray())

# Chuyển đổi nhãn dự đoán thành tên của chủ đề
predicted_category = label_encoder.inverse_transform(predicted_category_encoded.argmax(axis=1))

print(f"Predicted Category: {predicted_category[0]}")
