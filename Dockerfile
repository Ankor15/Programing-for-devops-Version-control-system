# Gunakan image Python sebagai base image
FROM python:3.9-slim

WORKDIR /app

# Salin file requirements.txt dan install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Salin file aplikasi ke dalam container
COPY . /app/

# Tentukan perintah untuk menjalankan aplikasi
CMD ["python", "app.py"]
