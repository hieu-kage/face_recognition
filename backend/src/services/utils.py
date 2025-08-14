import numpy as np
from sqlmodel import select
from src.models import User, Face_embedding
from src.database.database import get_session
from typing import Optional, Tuple
import cv2
import firebase_admin
from firebase_admin import credentials, storage
import tempfile
import os

# Khởi tạo Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "storageBucket": "your-bucket-name.appspot.com"
})

class Attendance:
    def __init__(self, threshold=23):
        self.threshold = threshold
        self.known_encodings, self.known_users, self.known_image_paths = self.load_data_from_db()

        from insightface.app import FaceAnalysis
        self.face_app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider", "CUDAExecutionProvider"])
        self.face_app.prepare(ctx_id=0)

    def load_data_from_db(self):
        known_encodings = []
        known_users = []
        known_image_paths = []

        with get_session() as session:
            statement = select(Face_embedding, User).join(User, Face_embedding.user_id == User.id)
            results = session.exec(statement).all()

            for face_emb, user in results:
                embedding = np.array(face_emb.face_embedding) if isinstance(face_emb.face_embedding, list) else face_emb.face_embedding
                known_encodings.append(embedding)
                known_users.append(user)
                known_image_paths.append(face_emb.image_path)  # Lấy path ảnh từ DB

        return known_encodings, known_users, known_image_paths

    def recognize_face_from_image(self, image: np.ndarray) -> Optional[Tuple[User, np.ndarray, np.ndarray]]:
        results = self.face_app.get(image)

        if not results:
            return None

        largest_face = max(results, key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]))
        matched_user, matched_path = self._match_embedding(largest_face.embedding)

        if matched_user is None:
            return None

        # Tải ảnh từ Storage
        matching_image = self._download_image_from_storage(matched_path)
        return matched_user, image, matching_image

    def _match_embedding(self, embedding: np.ndarray) -> Tuple[Optional[User], Optional[str]]:
        if len(self.known_encodings) == 0:
            return None, None

        distances = np.linalg.norm(np.array(self.known_encodings) - embedding, axis=1)
        min_dist = np.min(distances)
        min_index = np.argmin(distances)
        if min_dist < self.threshold:
            return self.known_users[min_index], self.known_image_paths[min_index]
        else:
            return None, None

    def _download_image_from_storage(self, image_path: str) -> Optional[np.ndarray]:
        try:
            bucket = storage.bucket()
            blob = bucket.blob(image_path)

            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                blob.download_to_filename(tmp_file.name)
                tmp_path = tmp_file.name

            img = cv2.imread(tmp_path)
            os.remove(tmp_path)
            return img
        except Exception as e:
            print(f"Lỗi tải ảnh từ Firebase: {e}")
            return None
