# NOTE:
# Docker pull max gets reached very quickly when using the dockerhub image.
# Pushing a retagged miniconda image to a github repo ommits this problem.
# 
# The latest miniconda3 images seem to be buggy and lead to errors.
# https://github.com/conda/conda/issues/13560
# Thus we use an older image version where this bug does not occur.
# TODO: Update this image to the latest version once this bug is fixed by conda.
# Buggy images: 24.4.0-0, 24.3.0-0, 24.1.2-0 (maybe more)
#FROM ghcr.io/oakestra/addon-flops/aux-miniconda3:23.10.0-1
#FROM ghcr.io/oakestra/addon-flops/aux-miniconda3:23.10.0-1_arm64
FROM docker.io/continuumio/miniconda3:23.10.0-1
LABEL org.opencontainers.image.source=https://github.com/oakestra/addon-flops

RUN apt-get update && apt-get install -y \
        # Seems to be necessary for arm64
        gcc python3-dev \
        # Optinal development dependencies:
        vim tree &&\
    apt-get clean

COPY . /fl_base
WORKDIR /fl_base
RUN rm Dockerfile requirements.txt

RUN conda env update --file ./conda.yaml &&\
    # https://flower.dev/docs/framework/how-to-install-flower.html
    conda config --add channels conda-forge &&\
    conda config --set channel_priority strict &&\
    conda install -y \
        # NOTE: This flwr version is the latest one that is available for the current base image.
        flwr=1.8.0 \
        pydantic~=2.7.1 \
        # NOTE: This dependency could be isolated and only used in the Learner.
        pillow~=10.4.0

# NOTE: For dependencies that cannot be installed via conda yet.    
COPY requirements.txt .
RUN pip install -r requirements.txt

# https://flower.dev/docs/framework/ref-telemetry.html
ENV FLWR_TELEMETRY_ENABLED=0

# NOTE: If you place this ARG at the very top, before the FROM it will not work.
# The reason is that this ARG is part of another "context".
# There is a "context" switch after every FROM statement.
# See multistage docker builds for more.
ARG ML_MODEL_FLAVOR
ENV ML_MODEL_FLAVOR=${ML_MODEL_FLAVOR}
