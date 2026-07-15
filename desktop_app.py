import cv2
import numpy as np
import mss
import time
import os
from ultralytics import YOLO

# Từ điển ánh xạ Class ID sang tên Tiếng Việt (Không dấu để tương thích với cv2.putText)
CLASS_NAMES_VN = {
    0: "W.224 - Duong nguoi di bo",
    1: "W.205c - Nga ba ben phai",
    2: "P.102 - Cam di nguoc chieu",
    3: "R.302a - Phai di vong sang phai",
    4: "W.205a - Giao nhau duong dong cap",
    5: "W.207 - Giao nhau duong khong uu tien",
    6: "W.201a - Ngoat nguy hiem ben trai",
    7: "P.123a - Cam re trai",
    8: "I.434a - Ben xe buyt",
    9: "R.303 - Giao nhau chay theo vong xuyen",
    10: "P.130 - Cam dung va do xe",
    11: "I.409 - Cho quay xe",
    12: "R.415a - Bien gop lan duong",
    13: "W.245a - Di cham",
    14: "P.106a - Cam xe tai",
    15: "W.203c - Duong bi thu hep phia phai",
    16: "P.117 - Gioi han chieu cao",
    17: "P.124a - Cam quay dau",
    18: "P.107 - Cam o to khach va tai",
    19: "P.124d - Cam re phai va quay dau",
    20: "P.103a - Cam o to",
    21: "W.203b - Duong bi thu hep phia trai",
    22: "W.221b - Go giam toc phia truoc",
    23: "P.111 - Cam xe hai va ba banh",
    24: "P.129 - Kiem tra",
    25: "S.505a - Chi danh cho xe may",
    26: "W.246a - Chuong ngai vat phia truoc",
    27: "W.225 - Tre em",
    28: "S.505a - Xe tai va xe cong",
    29: "P.104 - Cam mo to va xe may",
    30: "S.505a - Chi danh cho xe tai",
    31: "Camera - Duong co camera giam sat",
    32: "P.123b - Cam re phai",
    33: "W.202b - Nhieu cho ngoat nguy hiem",
    34: "B.8a - Cam xe so-mi ro-mooc",
    35: "P.137 - Cam re trai va phai",
    36: "P.139 - Cam di thang va re phai",
    37: "W.205b - Nga ba ben trai",
    38: "P.127 - Gioi han toc do (50km/h)",
    39: "P.127 - Gioi han toc do (60km/h)",
    40: "P.127 - Gioi han toc do (80km/h)",
    41: "P.127 - Gioi han toc do (40km/h)",
    42: "R.301e - Cac xe chi duoc re trai",
    43: "W.239b - Chieu cao tinh khong",
    44: "W.233 - Nguy hiem khac",
    45: "I.407a - Duong mot chieu",
    46: "P.131a - Cam do xe",
    47: "P.124b1 - Cam o to quay dau",
    48: "W.210 - Giao nhau duong sat co rao chan",
    49: "P.124c - Cam re trai va quay dau",
    50: "W.201b - Cho ngoat nguy hiem vong ben phai",
    51: "W.246c - Vong tranh sang ben phai"
}

def main():
    print("==================================================")
    print(" AI TRAFFIC SIGN RECOGNITION - SCREEN CAPTURE MODE")
    print("==================================================")
    print("[INFO] Đang tải mô hình YOLOv8...")
    
    # Tải mô hình
    model_path = r"models\best_traffic_sign_model.pt"
    try:
        model = YOLO(model_path)
        print(f"[INFO] Tải mô hình thành công từ {model_path}")
    except Exception as e:
        print(f"[LỖI] Không thể tải mô hình: {e}")
        return

    # Khởi tạo đối tượng mss để chụp màn hình
    sct = mss.mss()
    
    # Chọn màn hình để chụp. sct.monitors[1] thường là màn hình chính.
    monitor = sct.monitors[1]
    
    # Tuỳ chỉnh vùng màn hình muốn chụp (Ví dụ: Chụp góc trên cùng bên trái 800x600)
    # Nếu muốn chụp toàn màn hình, giữ nguyên monitor. 
    # Ở đây ta lấy khung hình 1024x768 giữa màn hình để đỡ lag và test dễ hơn với Youtube
    # Sử dụng khung hình 800x600 để khung chụp nhỏ gọn hơn, không bị chạm tới taskbar
    width = 800
    height = 600
    
    # Đảm bảo không bị lỗi index out of bounds
    if monitor["width"] < width: width = monitor["width"]
    if monitor["height"] < height + 80: height = monitor["height"] - 80 # Trừ hao taskbar
    
    left = monitor["left"] + (monitor["width"] - width) // 2
    # Căn giữa theo chiều dọc nhưng nhích lên 1 chút (trừ 100px)
    top = monitor["top"] + (monitor["height"] - height) // 2 - 100
    if top < monitor["top"]: top = monitor["top"]
    
    capture_bbox = {'top': top, 'left': left, 'width': width, 'height': height}
    
    print(f"[INFO] Bắt đầu nhận diện trên vùng màn hình {width}x{height}...")
    print("[INFO] Nhấn phím 'q' trên cửa sổ Camera để thoát.")

    window_name = "Screen Capture - YOLOv8 (Press 'q' to exit)"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    # Thu nhỏ cửa sổ hiển thị xuống 1/2 để không đè lên vùng đang quay ở giữa màn hình
    cv2.resizeWindow(window_name, width // 2, height // 2)
    # Di chuyển cửa sổ ra góc trên cùng bên trái
    cv2.moveWindow(window_name, 0, 0)

    while True:
        # 1. Chụp ảnh màn hình (chế độ Live View)
        sct_img = sct.grab(capture_bbox)
        img = np.array(sct_img)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        
        # 2. Hiển thị Live View (Chưa chạy YOLO để nhẹ máy và dễ căn chỉnh vùng chụp)
        live_img = img.copy()
        cv2.putText(live_img, "LIVE VIEW - Nhan 'c' de chup va nhan dien, 'q' de thoat", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow(window_name, live_img)

        # 3. Lắng nghe bàn phím
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):
            # 4. Khi nhấn 'c', tiến hành phân tích bằng YOLO trên khung hình đang đứng
            print("[INFO] Đang phân tích hình ảnh...")
            results = model.predict(source=img, conf=0.25, verbose=False)
            
            annotated_img = img.copy()
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                    cls_id = int(box.cls[0].item())
                    conf = float(box.conf[0].item())
                    cls_name = CLASS_NAMES_VN.get(cls_id, model.names[cls_id])
                    label = f"{cls_name} {conf:.2f}"
                    
                    cv2.rectangle(annotated_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                    cv2.rectangle(annotated_img, (x1, y1 - 25), (x1 + w, y1), (0, 0, 0), -1)
                    cv2.putText(annotated_img, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Lưu ảnh kết quả (trước khi vẽ dòng hướng dẫn màu đỏ lên trên)
            save_dir = "runs/captures"
            os.makedirs(save_dir, exist_ok=True)
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            save_path = os.path.join(save_dir, f"capture_{timestamp}.jpg")
            cv2.imwrite(save_path, annotated_img)
            print(f"[INFO] Đã lưu ảnh kết quả vào: {save_path}")

            # Hiển thị ảnh đã đóng băng
            cv2.putText(annotated_img, "KET QUA - Nhan phim bat ky de tiep tuc, 'q' de thoat", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.imshow(window_name, annotated_img)
            
            print("[INFO] Đã hiển thị kết quả. Nhấn phím bất kỳ trên cửa sổ OpenCV để tiếp tục.")
            # Chờ người dùng nhấn phím để tiếp tục quay lại Live View
            wait_key = cv2.waitKey(0) & 0xFF
            if wait_key == ord('q'):
                break

    # Dọn dẹp bộ nhớ
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
