nfs-server:
  image: gists/nfs-server
  container_name: nfs-server
  ports:
    - "2049:2049"
  # https://docs.docker.com/engine/reference/run/#runtime-privilege-and-linux-capabilities
  cap_add:
    - SYS_ADMIN
    - SETPCAP
  environment:
    - "NFS_DOMAIN=ip" # The visitor IP range
  volumes:
    - /your/path:/nfs-share
  restart: always