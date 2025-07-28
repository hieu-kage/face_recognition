from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    face_images: List["FaceImage"] = Relationship(back_populates="user")
    attendances: List["Attendance"] = Relationship(back_populates="user")