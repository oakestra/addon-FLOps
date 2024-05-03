# Notes:
# Docker pull max gets reached very quickly when using the dockerhub image.
# By pushing the retagged miniconda image to a github repo ommits this problem.
# 
# The latest miniconda3 images seem to be buggy and leads to errors.
# https://github.com/conda/conda/issues/13560
# Thus we use an older image version where this bug does not occur.
# TODO update this image to the latest version once this bug is fixed by conda.
# Buggy images: 24.3.0-0, 24.1.2-0 (maybe more)
FROM ghcr.io/malyuk-a/miniconda3:23.10.0-1

COPY . /fl_base
WORKDIR /fl_base
RUN rm Dockerfile requirements.txt

RUN conda env update --file ./conda.yaml &&\
    # https://flower.dev/docs/framework/how-to-install-flower.html
    conda config --add channels conda-forge &&\
    conda config --set channel_priority strict &&\
    # Note: This flwr version is the latest one that is available for the current base image.
    conda install flwr=1.8.0 -y

# Note: For dependencies that cannot be installed via conda yet.    
COPY requirements.txt .
RUN pip install -r requirements.txt

# https://flower.dev/docs/framework/ref-telemetry.html
ENV FLWR_TELEMETRY_ENABLED=0

