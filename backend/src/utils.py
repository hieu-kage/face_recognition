import os
import cv2
import pickle
import numpy as np
from datetime import datetime
from insightface.app import FaceAnalysis
from collections import defaultdict

class Attendance:
    def __init__(self, pkl_path="embeddings/encodings.pkl", threshold=0.6, log_path="attendance.csv"):
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
        distances = []
        for known_emb in self.known_encodings:
            dist = np.linalg.norm(embedding - known_emb)
            distances.append(dist)

        min_dist = min(distances)
        avg_dist = np.mean(distances)
        min_index = distances.index(min_dist)
        identity = self.known_names[min_index] if min_dist <= self.threshold else "Unknown"
        best_match_name = self.known_names[min_index]

        # Gom theo người
        person_dist_map = defaultdict(list)
        for name, dist in zip(self.known_names, distances):
            person_dist_map[name].append(dist)

        print(f"\n👤 Người gần nhất: {best_match_name} (min_dist = {min_dist:.4f})")
        print(f"📊 Trung bình theo từng người:")
        for name, dists in person_dist_map.items():
            avg = np.mean(dists)
            min_d = np.min(dists)
            print(f"  - {name}: {avg:.4f} (min: {min_d:.4f})")

        return identity, min_dist

    def process_frame(self, frame):
        faces = self.face_app.get(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))  # InsightFace cần RGB
        names = []

        for face in faces:
            x1, y1, x2, y2 = map(int, face.bbox)
            embedding = face.embedding
            name, dist = self.recognize_face(embedding)
            names.append(name)

            label = f"{name} ({dist:.2f})" if name != "Unknown" else "Unknown"
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

            if name != "Unknown":
                self.log_attendance(name)

        return frame, names

    def log_attendance(self, name):
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        print(f"[LOG] {name} đã điểm danh lúc {time_str}")

# =====================
# TEST bằng webcam
# =====================
def main():
    attendance = Attendance(
        pkl_path=r"F:\h\c++\kythuatdohoa\face_recognition\backend\embeddings\encodings.pkl"
    )

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Không thể mở webcam")
        return

    print("🎥 Đang chạy camera... Nhấn 'q' để thoát")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        processed_frame, _ = attendance.process_frame(frame)  # input frame BGR, output BGR
        cv2.imshow("Attendance System", processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
