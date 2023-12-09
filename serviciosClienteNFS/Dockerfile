FROM python:3.8

ARG NFS_SERVER_IP
ARG NFS_SHARED_FOLDER

RUN apt-get update && apt-get install -y nfs-common

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Crea el directorio /mnt/nfs
RUN mkdir -p /mnt/nfs

# Monta el sistema de archivos NFS durante el CMD
CMD ["sh", "-c", "mount -v -t nfs3 $NFS_SERVER_IP:$NFS_SHARED_FOLDER /mnt/nfs && python manage.py runserver 0.0.0.0:8000"]
