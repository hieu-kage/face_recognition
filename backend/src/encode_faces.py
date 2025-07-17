import os
import cv2
import pickle
import numpy as np
from tqdm import tqdm
from insightface.app import FaceAnalysis

# =====================
# CONFIG
# =====================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "data", "face_dataset")
SAVE_PATH = os.path.join(BASE_DIR, "embeddings", "encodings.pkl")

# =====================
# INIT InsightFace
# =====================
face_app = FaceAnalysis(name="buffalo_l", providers=["CUDAExecutionProvider", "CPUExecutionProvider"])
face_app.prepare(ctx_id=0)

# =====================
# LOAD EXISTING DATA
# =====================
if os.path.exists(SAVE_PATH):
    with open(SAVE_PATH, "rb") as f:
        face_data = pickle.load(f)
    print(f"🧠 Đã tải dữ liệu cũ từ: {SAVE_PATH}")
else:
    face_data = {}
    print("📂 Chưa có file encoding cũ, bắt đầu mới.")

# =====================
# ENCODE ẢNH MỚI
# =====================
new_count = 0
skipped = 0

for person_name in tqdm(os.listdir(DATASET_DIR), desc="🔍 Quét dữ liệu khuôn mặt"):
    person_dir = os.path.join(DATASET_DIR, person_name)
    if not os.path.isdir(person_dir):
        continue

    # Khởi tạo nếu chưa có
    if person_name not in face_data:
        face_data[person_name] = {}

    for image_name in os.listdir(person_dir):
        if not image_name.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        if image_name in face_data[person_name]:
            print(f"[⏭️] Bỏ qua: {person_name}/{image_name} đã có.")
            skipped += 1
            continue

        image_path = os.path.join(person_dir, image_name)
        img = cv2.imread(image_path)

        if img is None:
            print(f"[❌] Không đọc được ảnh: {image_path}")
            continue

        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        faces = face_app.get(rgb)

        if faces:
            embedding = faces[0].embedding
            face_data[person_name][image_name] = embedding
            new_count += 1
            print(f"[✅] Đã mã hoá: {person_name}/{image_name}")
        else:
            print(f"[⚠️] Không phát hiện mặt: {person_name}/{image_name}")

# =====================
# LƯU FILE
# =====================
os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
with open(SAVE_PATH, "wb") as f:
    pickle.dump(face_data, f)

# =====================
# TỔNG KẾT
# =====================
total_embeddings = sum(len(v) for v in face_data.values())
print(f"\n📦 Đã lưu tổng cộng {total_embeddings} embeddings vào: {SAVE_PATH}")
print(f"🆕 Thêm mới: {new_count} ảnh | ⏭️ Bỏ qua: {skipped} ảnh")
