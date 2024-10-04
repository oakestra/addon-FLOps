FROM python:3.10-slim-buster

RUN apt-get update &&\
    apt-get install -y \
        git \
        wget \
        libnss3-tools &&\
    apt-get clean &&\
    pip install poetry~=1.8.2

# NOTE: First install the dependencies in a seperate layer to improve docker layer caching.
# Thus making building and pushing faster by reusing the dependency layer.
COPY pyproject.toml pyproject.toml
RUN poetry lock && poetry install --no-root

WORKDIR /flops_manager
COPY flops_manager /flops_manager
RUN poetry install

# TRUE for verbose logging
ENV FLASK_ENV=development
ENV FLASK_DEBUG=TRUE

ENV FLOPS_MANAGER_PORT=5072
ENV FLOPS_IMAGE_REGISTRY_PORT=5073
ENV FLOPS_MQTT_BROKER_PORT=9027

EXPOSE $FLOPS_MANAGER_PORT
EXPOSE $FLOPS_IMAGE_REGISTRY_PORT
EXPOSE $FLOPS_MQTT_BROKER_PORT

ENV FLOPS_DB_PORT=10027

ENV FLOPS_MQTT_BROKER_URL=flops_mqtt

ENV SYSTEM_MANAGER_PORT=10000

RUN poetry add git+https://github.com/oakestra/addon-FLOps.git@main#subdirectory=utils_library

CMD ["poetry", "run", "python", "main.py"]
