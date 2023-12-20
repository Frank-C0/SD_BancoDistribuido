#!/bin/sh

# Monta el sistema de archivos NFS
echo $NFS_SERVER_IP:$NFS_SHARED_FOLDER
mount -v -t nfs -o vers=4,port=2049 $NFS_SERVER_IP:$NFS_SHARED_FOLDER /mnt/nfs/

# Ejecuta el comando CMD proporcionado
exec "$@"
