FROM python:3.12-slim

# Set environment variables untuk Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Instal dependensi (pastikan requirements.txt sudah di-generate via pip freeze di env lokal)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pymysql cryptography gunicorn

# Copy seluruh source code
COPY . .

EXPOSE 5000

ENV FLASK_APP="apps.app:create_app()"
ENV FLASK_ENV=production

# Gunakan Flask run karena app.py Anda tidak memiliki baris `app.run()`
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]