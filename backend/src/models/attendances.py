from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class Attendance(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    image_path: Optional[str]  # đường dẫn ảnh log ra
    status: Optional[str] = Field(default="present")  # ví dụ: present, late, absent

    user_id: int = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="attendances")