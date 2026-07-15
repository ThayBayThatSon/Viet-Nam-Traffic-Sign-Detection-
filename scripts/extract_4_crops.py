import cv2
from ultralytics import YOLO
import json

# 1. Crop 4 images from val_batch0_pred.jpg
img_path = r'c:\FPT\SU2026\CPV301\PE\runs\detect\traffic_sign_model\val_batch0_pred.jpg'
img = cv2.imread(img_path)

h, w, _ = img.shape
h_step = h // 4
w_step = w // 4

crops = []
# We will just take the 4 images in the first row
for i in range(4):
    crop = img[0:h_step, i*w_step:(i+1)*w_step]
    crop_path = fr'c:\FPT\SU2026\CPV301\PE\runs\detect\traffic_sign_model\val_crop_new_{i+1}.jpg'
    cv2.imwrite(crop_path, crop)
    crops.append(crop_path)

# 2. Run YOLO to find out what is in them
model = YOLO(r"models\best_traffic_sign_model.pt")

results_info = []
for idx, crop_path in enumerate(crops):
    res = model(crop_path)
    # Get the names of the detected classes
    names = model.names
    detected = []
    if len(res) > 0 and len(res[0].boxes) > 0:
        for c in res[0].boxes.cls:
            detected.append(names[int(c)])
    results_info.append({"image": f"val_crop_new_{idx+1}.jpg", "detected": detected})

print(json.dumps(results_info))
