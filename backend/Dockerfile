# Use a lightweight Python image for the final stage to keep the image size small
FROM python:3.11-slim as final

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt to leverage Docker's cache
COPY requirements.txt .

# Install dependencies. Use --no-cache-dir to keep the image size down.
RUN pip install --no-cache-dir -r requirements.txt

# --- This is the key change to fix the OOM error ---
# Download the 'buffalo_l.zip' model during the build
# This avoids the application downloading it at runtime.
RUN apt-get update && apt-get install -y --no-install-recommends wget unzip && \
    mkdir -p /root/.insightface/models && \
    wget -O /root/.insightface/models/buffalo_l.zip https://github.com/deepinsight/insightface/releases/download/v0.7/buffalo_l.zip && \
    unzip /root/.insightface/models/buffalo_l.zip -d /root/.insightface/models && \
    rm /root/.insightface/models/buffalo_l.zip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the rest of your application source code
COPY . .

# Expose the port that Uvicorn will listen on
EXPOSE 8000

# Use a production-ready command. --reload is for development only
# and can cause memory issues in production.
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]