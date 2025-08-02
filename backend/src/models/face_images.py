from sqlmodel import SQLModel, Field, Relationship,Column
from sqlalchemy import JSON
from typing import List, Optional
from sqlalchemy import LargeBinary
import numpy as np

class Face_embedding(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    image_path: str  # Đường dẫn ảnh gốc nếu cần
    face_embedding: List[float] = Field(sa_column=Column(JSON))
    user: "User" = Relationship(back_populates="face_embedding")