# image_service.py
import os
import cv2
import numpy as np
import firebase_admin
from firebase_admin import credentials, storage
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

FIREBASE_KEY = os.getenv("FIREBASE_KEY")
FIREBASE_BUCKET = os.getenv("FIREBASE_BUCKET")

# Khởi tạo Firebase chỉ 1 lần
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_KEY)
    firebase_admin.initialize_app(cred, {
        "storageBucket": FIREBASE_BUCKET
    })

def download_image_from_storage(image_path: str):
    """
    Tải ảnh từ Firebase Storage và trả về numpy array
    :param image_path: Đường dẫn trong bucket (vd: 'face_dataset/Nguyen Van A/Nguyen Van A_1.jpg')
    :return: np.ndarray hoặc None nếu lỗi
    """

    try:
        bucket = storage.bucket()
        image_path="image/"+image_path
        blob = bucket.blob(image_path)
        print(f"[DEBUG] Downloading image from: {image_path}")
        img_bytes = blob.download_as_bytes()
        img_array = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        return img
    except Exception as e:
        print(f"Lỗi tải ảnh từ Firebase: {e}")
        return None
