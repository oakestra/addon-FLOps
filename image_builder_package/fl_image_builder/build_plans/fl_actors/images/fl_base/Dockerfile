# NOTE:
# Docker pull max gets reached very quickly when using the dockerhub image.
# Pushing a retagged miniconda image to a github repo ommits this problem.
FROM ghcr.io/oakestra/addon-flops/aux-miniconda3:24.11.1-0
LABEL org.opencontainers.image.source=https://github.com/oakestra/addon-flops

RUN apt-get update && apt-get install -y \
        # Seem to be necessary for arm64.
        gcc python3-dev \
        # Necessary to avoid issues with conda/mamba.
        libarchive13 \
        # Optional development dependencies:
        vim tree &&\
    apt-get clean

COPY . /fl_base
WORKDIR /fl_base
RUN rm Dockerfile requirements.txt

RUN conda install -n base conda-libmamba-solver &&\
    # https://conda.io/projects/conda/en/latest/dev-guide/deep-dives/solvers.html
    # https://conda.github.io/conda-libmamba-solver/user-guide/
    conda config --set solver libmamba &&\
    # https://flower.dev/docs/framework/how-to-install-flower.html
    conda config --add channels conda-forge &&\
    conda config --set channel_priority strict &&\
    conda env update --file ./conda.yaml &&\
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
