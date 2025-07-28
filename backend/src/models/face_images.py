from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from sqlalchemy import LargeBinary
import numpy as np

class FaceImage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    image_path: str  # Đường dẫn ảnh gốc nếu cần
    face_embedding: bytes  # Dùng để lưu vector nhúng khuôn mặt
    user: "User" = Relationship(back_populates="face_images")