# IMPORTANT!: Needs to be run with --privileged otherwise errors occur.
# The base image has to support the following:
# - A buildah version (apt) that has the "build" command (older versions don't have it yet)
# - Python (version 3.10+)
# - MLflow (normal not skinny version)
# NOTE: This combination is surprisingly rare.
FROM ghcr.io/oakestra/addon-flops/aux-miniconda3:24.4.0-0
LABEL org.opencontainers.image.source=https://github.com/oakestra/addon-flops
WORKDIR /image_builder

RUN apt-get update && apt-get install -y \
        # Mandatory dependencies:
        #git wget qemu-user-static binfmt-support buildah \
        #git wget qemu-user-static buildah \
        #git wget qemu-user-binfmt qemu-user-static buildah \
        git wget buildah \
        # Optional development dependencies:
        vim tree &&\
    apt-get clean

# RUN apt-get update
# RUN apt-get install -y qemu-user-binfmt
# RUN apt-get install -y qemu-user-static

# Enable Emulation properly to be able to build multi-platform images.
# NOTE: This might not be a great solutions nor is it guaranteed to work on arm machines.
#RUN update-binfmts --enable qemu-arm || update-binfmts --enable qemu-x86_64
#RUN update-binfmts --enable qemu-arm

RUN conda install -y \
        requests>=2.28.1 \
        gitpython>=3.1.42\
        mlflow>=2.12.1

RUN pip install --no-cache-dir git+https://github.com/Malyuk-A/tmp_flops_utils.git@main

COPY /fl_image_builder /image_builder
