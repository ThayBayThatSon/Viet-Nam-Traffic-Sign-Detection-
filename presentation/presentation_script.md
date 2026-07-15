# Kịch bản Thuyết trình: Nhận diện Biển báo Giao thông Việt Nam (YOLOv8)

## Slide 1: Trang bìa (Giới thiệu)

**[Người thuyết trình 1]**
"Dạ, xin kính chào Thầy/Cô và các bạn. Chúng em là Nhóm 1. Hôm nay, nhóm chúng em rất vinh dự được trình bày về đồ án: **'Nhận diện Biển báo Giao thông Việt Nam sử dụng thuật toán YOLOv8'**.
Nhóm chúng em bao gồm 6 thành viên: Vũ, Minh, Sang, Khang, Nguyên, và Tiên. Sau đây, em xin phép đại diện nhóm bắt đầu phần trình bày của mình."

---

## Slide 2: Đặt vấn đề (Problem Statement)

**[Người thuyết trình 1]**
"Đầu tiên, vì sao nhóm lại chọn đề tài này?
Như mọi người cũng biết, điều kiện giao thông ở Việt Nam rất phức tạp, người lái xe đôi khi rất dễ bỏ lỡ hoặc không kịp nhìn thấy các biển báo, dẫn đến vi phạm hoặc nguy hiểm. Đồng thời, nhu cầu về các hệ thống hỗ trợ lái xe thông minh (ADAS) đang ngày càng tăng. Mục tiêu lớn nhất của nhóm là giảm thiểu tai nạn thông qua việc cảnh báo sớm.
Tuy nhiên, chúng em gặp phải một số thách thức: biển báo ở nước ta rất đa dạng, thường xuyên bị che khuất bởi cây cối, hoặc bị ảnh hưởng bởi thời tiết, ánh sáng. Do đó, bài toán đặt ra là cần một thuật toán nhận diện không chỉ chính xác mà còn phải **cực kỳ nhanh (real-time)**."

---

## Slide 3: Tổng quan Dữ liệu (Dataset Overview)

**[Người thuyết trình 1 hoặc 2]**
"Để giải quyết bài toán, chúng em sử dụng tập dữ liệu Biển báo Giao thông Việt Nam từ Kaggle.
Tập dữ liệu này tương đối đa dạng với **3.191 hình ảnh**, bao gồm **52 lớp biển báo** khác nhau, và tổng cộng có hơn **8.334 bounding boxes** (hộp bao quanh đối tượng).
Ở dưới là bảng chi tiết liệt kê một số lớp biển báo điển hình và số lượng phân bổ của chúng trong tập dữ liệu."

---

## Slide 4: Hình ảnh mẫu (Dataset Samples)

**[Người thuyết trình]**
"Đây là một số hình ảnh mẫu trích xuất từ tập dữ liệu. Như các bạn có thể thấy, các hình ảnh được chụp trong nhiều điều kiện thực tế khác nhau: góc chụp chéo, ngược sáng, hoặc bị mờ, phản ánh đúng tính chất phức tạp của giao thông đường phố."

---

## Slide 5: Công nghệ & Thuật toán (Technology & Algorithm)

**[Người thuyết trình]**
"Về mặt công nghệ, nhóm quyết định sử dụng mô hình **YOLOv8**, cụ thể là phiên bản **Nano (YOLOv8n)**.
YOLO (You Only Look Once) là một mạng nơ-ron tích chập (CNN) tiên tiến nhất hiện nay trong việc phát hiện đối tượng. Phiên bản Nano được nhóm lựa chọn vì nó cực kỳ nhẹ, tối ưu hóa tuyệt vời cho việc triển khai trên các thiết bị Edge (thiết bị biên) có cấu hình yếu như camera hành trình, mà vẫn đảm bảo được tốc độ xử lý."

---

## Slide 6: Chi tiết về YOLOv8 (Why we chose YOLOv8)

**[Người thuyết trình]**
"Vậy tại sao lại là YOLOv8?
Thứ nhất, nó **siêu nhanh**. Thuật toán này không chia ảnh ra phân tích từng phần chậm chạp mà nó 'nhìn' toàn bộ bức ảnh cùng một lúc, phát hiện đối tượng ngay lập tức.
Thứ hai, nó **độ chính xác cao** kể cả với các vật thể nhỏ hay bị mờ.
Và cuối cùng là sự **nhỏ gọn** giúp triển khai trực tiếp lên phần cứng trên ô tô. Thuật toán đã 'học' được hình dáng, màu sắc đặc trưng của hơn 50 loại biển báo Việt Nam qua hàng ngàn bức ảnh để đưa ra dự đoán."

---

## Slide 7: Quá trình Huấn luyện (Training Process)

**[Người thuyết trình]**
"Để có được mô hình, nhóm đã tiến hành huấn luyện (training) trong **50 Epochs** trên môi trường Google Colab với GPU.
Như Thầy/Cô và các bạn có thể quan sát trên biểu đồ Loss: các đường biểu diễn độ mất mát (Loss) giảm đều và hội tụ rất tốt ở cả tập Train và tập Validation. Điều này chứng tỏ mô hình học rất hiệu quả và hoàn toàn không có dấu hiệu bị quá khớp (Overfitting)."

---

## Slide 8: Kết quả Đánh giá (Evaluation Metrics & Confusion Matrix)

**[Người thuyết trình]**
"Kết quả đạt được thực sự rất ấn tượng.
Mô hình đạt chỉ số **mAP@50 lên đến 97.68%**. Chỉ số Recall đạt gần 97%, nghĩa là mô hình hầu như không bỏ sót các biển báo thực tế trên đường. Tỷ lệ Precision cũng đạt trên 89%, cho thấy khả năng dự đoán đúng rất cao.
Phía bên phải là Ma trận nhầm lẫn (Confusion Matrix). Trong đó các thông số True Positive, False Positive và False Negative minh họa chi tiết tỷ lệ dự đoán trúng, báo động giả, và bỏ sót vật thể."

---

## Slide 9: Hình ảnh Dự đoán trực quan (Visual Inference Results)

**[Người thuyết trình]**
"Đây là một vài kết quả dự đoán (Inference) trên tập Validation. Mọi người có thể thấy các khung bounding box bao quanh biển báo rất khít và điểm tin cậy (Confidence Score) hiển thị bên trên khung đều đạt mức cao."

---

## Slide 10: Chi tiết nhận diện thực tế (Visual Inference - Zoomed Detail 1)

**[Người thuyết trình]**
"Để minh chứng rõ hơn, nhóm đã trích xuất dự đoán trên một bức ảnh thực tế thô.
Mô hình không chỉ khoanh vùng chính xác mà còn phân loại đúng biển báo 'Cấm rẽ trái và quay đầu xe' (P.124c) mặc dù kích thước của biển báo trong khung hình tương đối nhỏ. Nó đáp ứng hoàn hảo yêu cầu phát hiện từ xa."

---

## Slide 11: Chi tiết nhận diện thực tế (Visual Inference - More Results)

**[Người thuyết trình]**
"Tương tự ở một ví dụ khác có background phức tạp hơn, có nhiều bảng hiệu quảng cáo và chi tiết thừa. Mô hình vẫn dễ dàng nhận ra và phân biệt được biển 'Cấm rẽ trái' và biển 'Giao nhau với đường đồng cấp'. Điều này chứng minh tính ứng dụng rất cao của mô hình."

---

## Slide 12: Demo trực tiếp (Live Demo)

**[Người thuyết trình]**
"Để chứng minh hệ thống hoạt động hiệu quả, nhóm đã tích hợp mô hình vào một ứng dụng Web App. Sau đây, xin mời Thầy/Cô và các bạn cùng xem phần Live Demo trực tiếp thao tác trên ứng dụng của nhóm để thấy rõ hơn quá trình upload hình ảnh và nhận diện tức thời."
*(Người thuyết trình thực hiện mở trang web Localhost:5000 và tiến hành demo)*

---

## Slide 13: Hạn chế & Hướng phát triển (Limitations & Future Work)

**[Người thuyết trình]**
"Mặc dù đạt kết quả tốt, nhưng nhóm cũng nhận ra một số hạn chế:

- **Mất cân bằng dữ liệu:** Một số loại biển báo hiếm có quá ít ảnh để huấn luyện, dẫn đến độ chính xác chưa đồng đều.
- Mô hình vẫn gặp khó trong điều kiện ánh sáng cực yếu, ngược sáng mạnh hoặc biển báo bị méo mó, che khuất quá 80%.

Do đó, **hướng phát triển** trong tương lai của nhóm là:

1. Thu thập và Data Augmentation (tăng cường dữ liệu) cho các lớp bị thiếu.
2. Triển khai mô hình thẳng lên các bo mạch nhúng như Raspberry Pi hay Jetson Nano để làm Dashcam thực thụ.
3. Tích hợp thêm hệ thống phát âm thanh cảnh báo bằng giọng nói cho tài xế."

---

## Slide 14: Lời cảm ơn & Q&A

**[Người thuyết trình]**
"Phần trình bày của Nhóm 1 đến đây là kết thúc. Chúng em xin chân thành cảm ơn Thầy/Cô và các bạn đã lắng nghe.
Tiếp theo, chúng em rất mong nhận được những góp ý cũng như những câu hỏi từ Thầy/Cô và các bạn ạ."
