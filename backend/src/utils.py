import os
import cv2
import pickle
import numpy as np
from datetime import datetime
from insightface.app import FaceAnalysis
from collections import defaultdict

class Attendance:
    def __init__(self, pkl_path="../embeddings/encodings.pkl", threshold=20, log_path="attendance.csv"):
        self.pkl_path = pkl_path
        self.threshold = threshold
        self.log_path = log_path

        # Khởi tạo InsightFace
        self.face_app = FaceAnalysis(name="buffalo_l", providers=["CUDAExecutionProvider", "CPUExecutionProvider"])
        self.face_app.prepare(ctx_id=0)

        # Load dữ liệu đã encode
        self.known_encodings, self.known_names = self.load_data()
        print(f"[INFO] Đã load {len(self.known_encodings)} embeddings từ {self.pkl_path}")

    def load_data(self):
        if not os.path.exists(self.pkl_path):
            raise FileNotFoundError(f"❌ Không tìm thấy file: {self.pkl_path}")
        with open(self.pkl_path, "rb") as f:
            data = pickle.load(f)

        encodings = []
        names = []
        for person_name, images in data.items():
            if isinstance(images, dict):
                for emb in images.values():
                    encodings.append(emb)
                    names.append(person_name)
            else:
                print(f"[⚠️] Dữ liệu người '{person_name}' không đúng định dạng, bỏ qua.")
        return encodings, names

    def recognize_face(self, embedding):


    def process_frame(self, frame):


        return frame, names

    def log_attendance(self, name):




