FROM python:3.10-slim-buster
LABEL org.opencontainers.image.source https://github.com/oakestra/oakestra

RUN apt-get update && apt-get install git wget libnss3-tools -y && apt-get clean && pip install poetry~=1.8.2

RUN wget https://github.com/FiloSottile/mkcert/releases/download/v1.4.4/mkcert-v1.4.4-linux-amd64 &&\
    mv mkcert-v1.4.4-linux-amd64 /usr/bin/mkcert &&\
    chmod +x /usr/bin/mkcert

# Note: First install the dependencies in a seperate layer to improve docker layer caching.
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

RUN poetry add git+https://github.com/Malyuk-A/tmp_flops_utils.git@main

CMD ["poetry", "run", "python", "main.py"]
