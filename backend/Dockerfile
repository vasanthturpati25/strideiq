FROM python:3.11-slim

WORKDIR /app

# System deps for OpenCV / MediaPipe + curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 libsm6 libxrender1 libxext6 libgl1 curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p media/uploads

CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn strideiq_project.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120"]