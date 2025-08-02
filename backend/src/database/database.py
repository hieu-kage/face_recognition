from sqlmodel import SQLModel, create_engine, Session,select
from dotenv import load_dotenv
from ..models import *
import os
# Load biến môi trường từ file .env
load_dotenv()

# Đọc biến môi trường
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Tạo URL kết nối MySQL
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Tạo engine
engine = create_engine(DATABASE_URL, echo=True)

# Hàm tạo bảng
def init_db():
    SQLModel.metadata.create_all(engine)

# Hàm tạo session
def get_session():
    with Session(engine) as session:
        yield session
