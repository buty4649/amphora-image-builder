FROM ubuntu
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y python-pip python-dib-utils python-yaml python-babel qemu libguestfs-tools kpartx debootstrap git curl sudo 
COPY . /src/
WORKDIR /src/
CMD ./build.sh
