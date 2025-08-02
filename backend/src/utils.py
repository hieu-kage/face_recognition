import os
import pickle
import numpy as np
from insightface.app import FaceAnalysis
from datetime import datetime

class Attendance:
    def __init__(self, pkl_path="embeddings/encodings.pkl", threshold=20):
        self.pkl_path = pkl_path
        self.threshold = threshold

        self.face_app = FaceAnalysis(name="buffalo_s", providers=["CUDAExecutionProvider", "CPUExecutionProvider"])
        self.face_app.prepare(ctx_id=0)

        self.known_encodings, self.known_names = self.load_data()

    def load_data(self):
        if not os.path.exists(self.pkl_path):
            raise FileNotFoundError(f"Không tìm thấy file: {self.pkl_path}")
        with open(self.pkl_path, "rb") as f:
            data = pickle.load(f)

        encodings = []
        names = []
        for person_name, images in data.items():
            if isinstance(images, dict):
                for emb in images.values():
                    encodings.append(emb)
                    names.append(person_name)
        return encodings, names

    def recognize_faces_from_image(self, image: np.ndarray):
        results = self.face_app.get(image)
        names = []

        for face in results:
            embedding = face.embedding
            name = self._match_embedding(embedding)
            names.append(name)
        return names

    def _match_embedding(self, embedding):
        distances = np.linalg.norm(np.array(self.known_encodings) - embedding, axis=1)
        min_dist = np.min(distances)
        min_index = np.argmin(distances)

        if min_dist < self.threshold:
            return self.known_names[min_index]
        else:
            return "Unknown"

