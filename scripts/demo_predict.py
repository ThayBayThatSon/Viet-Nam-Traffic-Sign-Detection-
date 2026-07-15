import cv2
# pyrefly: ignore [missing-import]
from ultralytics import YOLO
import sys

# Khởi tạo mô hình
# Đảm bảo file best_traffic_sign_model.pt nằm trong thư mục models
model_path = r"models\best_traffic_sign_model.pt"
try:
    model = YOLO(model_path)
    print(f"[INFO] Đã load thành công model từ {model_path}")
except Exception as e:
    print(f"[LỖI] Không thể load model. Vui lòng kiểm tra xem đã có file best.pt ở thư mục hiện tại chưa.\nLỗi chi tiết: {e}")
    sys.exit()

def predict_image(image_path):
    """Chạy nhận diện trên một ảnh tĩnh có sẵn"""
    print(f"[INFO] Đang nhận diện ảnh: {image_path}")
    results = model.predict(source=image_path, conf=0.5, save=False)
    
    # Hiển thị ảnh
    for r in results:
        annotated_img = r.plot()
        cv2.imshow("Traffic Sign Detection Result", annotated_img)
        
    print("[INFO] Nhấn phím bất kỳ trên cửa sổ ảnh để đóng.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    print("=== TRAFFIC SIGN RECOGNITION DEMO ===")
    print("Tính năng: Nhận diện Biển báo Giao thông qua Ảnh")
    img_path = input("Mời nhập đường dẫn đến file ảnh (ví dụ: test.jpg): ")
    
    if img_path.strip():
        predict_image(img_path.strip())
    else:
        print("Đường dẫn không hợp lệ. Vui lòng chạy lại.")
