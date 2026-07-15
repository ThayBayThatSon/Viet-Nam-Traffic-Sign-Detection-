import cv2
import numpy as np
import base64
from flask import Flask, request, jsonify, render_template
from ultralytics import YOLO

app = Flask(__name__)

# Từ điển ánh xạ Class ID sang tên Tiếng Việt chi tiết
CLASS_NAMES_VN = {
    0: "W.224 – Đường người đi bộ cắt ngang",
    1: "W.205c – Đường giao nhau (ngã ba bên phải)",
    2: "P.102 – Cấm đi ngược chiều",
    3: "R.302a – Phải đi vòng sang bên phải",
    4: "W.205a – Giao nhau với đường đồng cấp",
    5: "W.207 – Giao nhau với đường không ưu tiên",
    6: "W.201a – Chỗ ngoặt nguy hiểm vòng bên trái",
    7: "P.123a – Cấm rẽ trái",
    8: "I.434a – Bến xe buýt",
    9: "R.303 – Nơi giao nhau chạy theo vòng xuyến",
    10: "P.130 – Cấm dừng và đỗ xe",
    11: "I.409 – Chỗ quay xe",
    12: "R.415a – Biển gộp làn đường theo phương tiện",
    13: "W.245a – Đi chậm",
    14: "P.106a*Xe tải – Cấm xe tải",
    15: "W.203c – Đường bị thu hẹp về phía phải",
    16: "P.117* – Giới hạn chiều cao",
    17: "P.124a* – Cấm quay đầu",
    18: "P.107 – Cấm ô tô khách và ô tô tải",
    19: "P.124d – Cấm rẽ phải và quay đầu",
    20: "P.103a – Cấm ô tô",
    21: "W.203b – Đường bị thu hẹp về phía trái",
    22: "W.221b – Gồ giảm tốc phía trước",
    23: "P.111 – Cấm xe hai và ba bánh",
    24: "P.129 – Kiểm tra",
    25: "S.505aXe máy – Chỉ dành cho xe máy",
    26: "W.246a – Chướng ngoại vật phía trước",
    27: "W.225 – Trẻ em",
    28: "S.505aXe tải và công – Xe tải và xe công",
    29: "P.104 – Cấm mô tô và xe máy",
    30: "S.505aXe tải – Chỉ dành cho xe tải",
    31: "Camera – Đường có camera giám sát",
    32: "P.123b – Cấm rẽ phải",
    33: "W.202b – Nhiều chỗ ngoặt nguy hiểm liên tiếp, chỗ đầu tiên sang phải",
    34: "B.8a – Cấm xe sơ-mi rơ-moóc",
    35: "P.137 – Cấm rẽ trái và phải",
    36: "P.139 – Cấm đi thẳng và rẽ phải",
    37: "W.205b – Đường giao nhau (ngã ba bên trái)",
    38: "P.127*50 – Giới hạn tốc độ (50km/h)",
    39: "P.127*60 – Giới hạn tốc độ (60km/h)",
    40: "P.127*80 – Giới hạn tốc độ (80km/h)",
    41: "P.127*40 – Giới hạn tốc độ (40km/h)",
    42: "R.301e – Các xe chỉ được rẽ trái",
    43: "W.239b* – Chiều cao tĩnh không thực tế",
    44: "W.233 – Nguy hiểm khác",
    45: "I.407a – Đường một chiều",
    46: "P.131a – Cấm đỗ xe",
    47: "P.124b1 – Cấm ô tô quay đầu xe (được rẽ trái)",
    48: "W.210 – Giao nhau với đường sắt có rào chắn",
    49: "P.124c – Cấm rẽ trái và quay đầu xe",
    50: "W.201b – Chỗ ngoặt nguy hiểm vòng bên phải",
    51: "W.246c – Chú ý chướng ngại vật – vòng tránh sang bên phải"
}
# Tải model 1 lần duy nhất khi khởi động server
model_path = r"models\best_traffic_sign_model.pt"
try:
    model = YOLO(model_path)
    print(f"[INFO] Đã load thành công model từ {model_path}")
except Exception as e:
    print(f"[LỖI] Không thể load model: {e}")
    model = None

@app.route('/')
def index():
    """Trang chủ giao diện Web"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """API Nhận diện ảnh gửi từ Frontend"""
    if model is None:
        return jsonify({'error': 'Chưa load được model (thiếu file best.pt)'}), 500
        
    if 'file' not in request.files:
        return jsonify({'error': 'Không tìm thấy file ảnh trong request'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'File rỗng'}), 400

    try:
        # Đọc dữ liệu ảnh từ luồng byte
        img_bytes = file.read()
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Dự đoán bằng YOLO (Giảm conf xuống 0.25 để bắt được biển báo bị sót)
        results = model.predict(source=img, conf=0.25, save=False, verbose=False)
        
        detections = []
        result_img = img # Mặc định là ảnh gốc
        
        # Xử lý kết quả trả về từ YOLO
        for r in results:
            result_img = r.plot() # Lấy ảnh đã vẽ khung (bounding box)
            
            # Trích xuất danh sách các biển báo tìm thấy
            for box in r.boxes:
                cls_id = int(box.cls[0].item())
                # Ánh xạ ID sang tên tiếng Việt chi tiết nếu có, ngược lại dùng tên gốc
                cls_name = CLASS_NAMES_VN.get(cls_id, model.names[cls_id])
                conf = float(box.conf[0].item())
                detections.append({'class': cls_name, 'confidence': round(conf, 2)})

        # Chuyển đổi ảnh numpy array sang Base64 để gửi về Frontend hiển thị ngay lập tức
        _, buffer = cv2.imencode('.jpg', result_img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return jsonify({
            'success': True,
            'image_base64': img_base64,
            'detections': detections
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Chạy Server trên cổng 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
