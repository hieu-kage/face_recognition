from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    student_id: str = Field(index=True, unique=True)
    face_embedding: List["Face_embedding"] = Relationship(back_populates="user")
    attendances: List["Attendance"] = Relationship(back_populates="user")