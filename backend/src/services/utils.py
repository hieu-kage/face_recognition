import numpy as np
from sqlmodel import select
from typing import Optional, Tuple
from ..models import User, Face_embedding
from ..database.database import get_session
from .firebase_services import download_image_from_storage
class Attendance:
    def __init__(self, threshold=23):
        """
        threshold: Ngưỡng khoảng cách embedding để quyết định có match hay không.
        """
        self.threshold = threshold
        # known_encodings: Danh sách embedding của các khuôn mặt đã biết
        # known_users: Danh sách object User tương ứng với mỗi embedding
        # known_image_paths: Danh sách đường dẫn ảnh gốc trong Firebase Storage cho mỗi embedding
        self.known_encodings, self.known_users, self.known_image_paths = self.load_data_from_db()

        from insightface.app import FaceAnalysis
        self.face_app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider", "CUDAExecutionProvider"])
        self.face_app.prepare(ctx_id=0)

    def load_data_from_db(self):
        """
        Load embedding, thông tin user và path ảnh gốc từ DB.
        Trả về:
            known_encodings: list[np.ndarray]
            known_users: list[User]
            known_image_paths: list[str]
        """
        known_encodings = []
        known_users = []
        known_image_paths = []

        with get_session() as session:
            statement = select(Face_embedding, User).join(User, Face_embedding.user_id == User.id)
            results = session.exec(statement).all()

            print(f"[DEBUG] Số bản ghi load từ DB: {len(results)}")
            for face_emb, user in results:
                embedding = np.array(face_emb.face_embedding) if isinstance(face_emb.face_embedding, list) else face_emb.face_embedding
                known_encodings.append(embedding)  # embedding vector
                known_users.append(user)           # object User ORM
                known_image_paths.append(face_emb.image_path)  # path ảnh gốc

                print(f"[DEBUG] Load user: {user.id} - {user.name}, image_path: {face_emb.image_path}")

        return known_encodings, known_users, known_image_paths

    def recognize_face_from_image(self, image: np.ndarray) -> Optional[Tuple[User, np.ndarray, np.ndarray]]:
        """
        Nhận diện khuôn mặt từ ảnh input.

        Trả về tuple:
            matched_user: User ORM object (thông tin người khớp)
            image: np.ndarray (ảnh input đang xử lý)
            matching_image: np.ndarray (ảnh gốc từ Firebase Storage của người đó)

        Nếu không match, trả về None.
        """
        results = self.face_app.get(image)

        if not results:
            print("[DEBUG] Không phát hiện khuôn mặt nào.")
            return None

        # Chọn khuôn mặt lớn nhất trong ảnh
        largest_face = max(results, key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]))
        matched_user, matched_path = self._match_embedding(largest_face.embedding)

        if matched_user is None:
            print("[DEBUG] Không tìm thấy user khớp.")
            return None

        print(f"[DEBUG] User match: {matched_user.id} - {matched_user.name}")
        print(f"[DEBUG] Image path từ DB: {matched_path}")

        # Tải ảnh gốc từ Firebase Storage
        matching_image = download_image_from_storage(matched_path)
        if matching_image is None:
            print("[DEBUG] Không tải được ảnh gốc từ Firebase.")

        return matched_user, image, matching_image

    def _match_embedding(self, embedding: np.ndarray) -> Tuple[Optional[User], Optional[str]]:
        """
        So sánh embedding input với các embedding đã biết.
        Trả về:
            matched_user: User ORM object nếu match, None nếu không match
            matched_path: str - path ảnh gốc trong Firebase Storage
        """
        if len(self.known_encodings) == 0:
            print("[DEBUG] Không có dữ liệu known_encodings.")
            return None, None

        # Tính khoảng cách Euclidean giữa embedding input và embedding đã biết
        distances = np.linalg.norm(np.array(self.known_encodings) - embedding, axis=1)
        min_dist = np.min(distances)
        min_index = np.argmin(distances)

        print(f"[DEBUG] Khoảng cách nhỏ nhất: {min_dist}")

        if min_dist < self.threshold:
            return self.known_users[min_index], self.known_image_paths[min_index]
        else:
            return None, None
