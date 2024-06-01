# IMPORTANT!: Needs to be run with --privileged otherwise errors occur.
# The base image has to support the following:
# - a buildah version (apt) that has the "build" command (older versions don't have it yet)
# - python (version 3.10+)
# - mlflow (normal not skinny version)
# Note: This combination is surprisingly rare.
FROM ghcr.io/malyuk-a/miniconda3:24.4.0-0
WORKDIR /image_builder

RUN apt-get update && apt-get install -y \
    # Mandatory dependencies:
    git wget buildah \
    # Optinal development dependencies:
    vim tree &&\
    rm -rf /var/lib/apt/lists/*

RUN conda install -y \
    requests>=2.28.1 \
    gitpython>=3.1.42\
    mlflow>=2.12.1

RUN pip install --no-cache-dir git+https://github.com/Malyuk-A/tmp_flops_utils.git@main

COPY /fl_image_builder /image_builder
