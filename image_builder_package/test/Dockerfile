FROM ghcr.io/oakestra/addon-flops/aux-miniconda3:24.4.0-0
WORKDIR /image_builder

RUN apt-get update && apt-get install -y \
        git wget buildah \
        # Optional development dependencies:
        #vim tree binfmt-support &&\
        vim tree &&\
    apt-get clean

#RUN apt-get update
# RUN apt-get install -y qemu-user-binfmt
#RUN apt-get install -y qemu-user-static

# RUN echo 'qemu-user-static' > /etc/binfmt.d/qemu-user-static.conf && \
#     update-binfmts --enable qemu-user-static

COPY dummy.Dockerfile /image_builder/dummy.Dockerfile

CMD buildah build --platform linux/arm64 --isolation=chroot -t dummy -f dummy.Dockerfile .
