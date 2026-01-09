FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/backend

WORKDIR /app

# ---------- SYSTEM DEPENDENCIES ----------
RUN apt-get update && apt-get install -y \
    ffmpeg \
    tesseract-ocr \
    libsm6 \
    libxext6 \
    libgl1 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# ---------- PYTHON DEPENDENCIES ----------
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ---------- APP FILES ----------
COPY backend ./backend
COPY frontend ./frontend
COPY data ./data

# ---------- SERVER ----------
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8080"]