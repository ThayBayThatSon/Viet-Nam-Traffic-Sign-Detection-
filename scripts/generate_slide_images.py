import cv2
from ultralytics import YOLO
import os

model = YOLO(r"models\best_traffic_sign_model.pt")
image_dir = r"data\archive\images"
output_dir = r"runs\detect\real_inference"

os.makedirs(output_dir, exist_ok=True)

found = False
for img_name in os.listdir(image_dir):
    if not img_name.endswith(('.jpg', '.png', '.jpeg')):
        continue
    
    img_path = os.path.join(image_dir, img_name)
    results = model.predict(source=img_path, conf=0.5, save=False, verbose=False)
    
    if len(results) > 0:
        res = results[0]
        if len(res.boxes) >= 2:
            classes = res.boxes.cls.cpu().numpy()
            unique_classes = set(classes)
            if len(unique_classes) >= 2:
                print(f"Found image with diverse detections: {img_name}")
                
                orig_img = cv2.imread(img_path)
                cv2.imwrite(os.path.join(output_dir, "original_2.jpg"), orig_img)
                
                pred_img = res.plot()
                cv2.imwrite(os.path.join(output_dir, "pred_2.jpg"), pred_img)
                
                boxes = res.boxes.xyxy.cpu().numpy()
                names = res.names
                
                idx_to_crop = []
                seen_cls = set()
                for i, c in enumerate(classes):
                    if c not in seen_cls:
                        seen_cls.add(c)
                        idx_to_crop.append(i)
                    if len(idx_to_crop) == 2:
                        break
                
                for k, idx in enumerate(idx_to_crop):
                    x1, y1, x2, y2 = map(int, boxes[idx])
                    h, w = orig_img.shape[:2]
                    x1 = max(0, x1 - 10)
                    y1 = max(0, y1 - 10)
                    x2 = min(w, x2 + 10)
                    y2 = min(h, y2 + 10)
                    
                    crop = orig_img[y1:y2, x1:x2]
                    cv2.imwrite(os.path.join(output_dir, f"crop_{k+3}.jpg"), crop)
                    print(f"Crop {k+1}: ID {int(classes[idx])} - {names[int(classes[idx])]}")
                
                found = True
                break

if not found:
    print("Could not find an image with diverse detections.")
