import pickle
import os

# Đường dẫn tới file encodings.pkl
PKL_PATH = os.path.join("../", "embeddings", "encodings.pkl")

# Đọc file và in ra danh sách tên
if os.path.exists(PKL_PATH):
    with open(PKL_PATH, "rb") as f:
        encodings, names = pickle.load(f)

    print(f"📦 Tổng số embeddings: {len(encodings)}")
    print("📋 Danh sách tên đã mã hoá:")
    for i, name in enumerate(names):
        print(f"{i+1:02d}. {name}")
else:
    print(f"❌ Không tìm thấy file: {PKL_PATH}")
