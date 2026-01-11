FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    tesseract-ocr \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# copy backend
COPY backend/app ./app

# copy frontend
COPY frontend ./frontend

ENV PYTHONPATH=/app

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]