# IMPORTANT!: Needs to be run with --privileged otherwise errors occur.
# Note: This python version comes with the proper apt listing to install buildah version 1.28.2(+)
# This buildah version is crucial to be able to run its "build" command.
FROM python:3.13.0a4-slim-bookworm
WORKDIR /image_builder

RUN apt-get update && apt-get install -y \
    # Mandatory dependencies:
    git wget buildah \
    # Optinal development dependencies:
    vim tree &&\
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY /fl_image_builder /image_builder
