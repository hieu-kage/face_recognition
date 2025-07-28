
from fastapi import FastAPI

from .route import image
from .database.database import init_db
from fastapi.middleware.cors import CORSMiddleware
# Tạo app FastAPI
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # hoặc chỉ định domain cụ thể, ví dụ: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức: GET, POST, OPTIONS, v.v.
    allow_headers=["*"],
)
# Khởi tạo database (tạo bảng nếu chưa có)
# Đăng ký router sách
init_db()
app.include_router(image.router)
