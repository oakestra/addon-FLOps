FROM python:3.10-slim-buster
LABEL org.opencontainers.image.source https://github.com/oakestra/oakestra

RUN apt-get update && apt-get install git wget libnss3-tools -y && apt-get clean && pip install poetry~=1.8.2 pip-tools

RUN wget https://github.com/FiloSottile/mkcert/releases/download/v1.4.4/mkcert-v1.4.4-linux-amd64 &&\
    mv mkcert-v1.4.4-linux-amd64 /usr/bin/mkcert &&\
    chmod +x /usr/bin/mkcert

# Note: Before switching to poetry it was enought to have a requirements.txt file and to install it before copying the files.
# Just calling "poetry install" is enough, however "poetry install" needs all package files to be already copied over into the container.
# During the "poetry install" call all dependencies listed in the pyproject.toml will be installed from scratch.
# If you are developing this package and need to regularly re-build this image, every little change will lead to a total dependency rebuild.
# To accelerate this process the requirements get extracted and installed before copying the package files.
# This makes efficient docker layer caching possible and regular rebuilds will be able to reuse the lengthy dependcy installation layers.
COPY pyproject.toml pyproject.toml
RUN python -m piptools compile -o requirements.txt pyproject.toml &&\
    pip install -r requirements.txt

COPY flops_manager /flops_manager
RUN poetry install

# TRUE for verbose logging
ENV FLASK_ENV=development
ENV FLASK_DEBUG=TRUE

ENV FLOPS_IMAGE_REGISTRY_PORT=5073
ENV FLOPS_MANAGER_PORT=5072
EXPOSE $FLOPS_MANAGER_PORT

ENV FLOPS_MQTT_BROKER_PORT=9027
ENV FLOPS_MQTT_BROKER_URL=flops_mqtt

ENV CAROOT=/etc/ssl

WORKDIR /flops_manager

CMD ["poetry", "run", "python", "main.py"]
