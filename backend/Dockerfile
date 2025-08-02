FROM python:3.11

# Tạo thư mục làm việc
WORKDIR /app

# Copy requirements trước để tận dụng cache
COPY requirements.txt .

# Cài thư viện
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends wget unzip && \
    mkdir -p /root/.insightface/models && \
    wget -O /root/.insightface/models/buffalo_l.zip https://github.com/deepinsight/insightface/releases/download/v0.7/buffalo_l.zip && \
    unzip /root/.insightface/models/buffalo_l.zip -d /root/.insightface/models && \
    rm /root/.insightface/models/buffalo_l.zip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# Copy toàn bộ source
COPY . .



# Chạy app FastAPI
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
