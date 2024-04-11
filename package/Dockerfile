FROM python:3.10-slim-buster
LABEL org.opencontainers.image.source https://github.com/oakestra/oakestra

WORKDIR /package_files
COPY . /package_files

RUN apt-get update && apt-get install git wget libnss3-tools -y && apt-get clean

RUN wget https://github.com/FiloSottile/mkcert/releases/download/v1.4.4/mkcert-v1.4.4-linux-amd64 &&\
    mv mkcert-v1.4.4-linux-amd64 /usr/bin/mkcert &&\
    chmod +x /usr/bin/mkcert

RUN pip install poetry~=1.8.2 && poetry install

# TRUE for verbose logging
ENV FLASK_ENV=development
ENV FLASK_DEBUG=TRUE

ENV FLOPS_IMAGE_REGISTRY_PORT=5073
ENV FLOPS_MANAGER_PORT=5072
EXPOSE $FLOPS_MANAGER_PORT

ENV FLOPS_MQTT_BROKER_PORT=9027
ENV FLOPS_MQTT_BROKER_URL=flops_mqtt

ENV CAROOT=/etc/ssl

WORKDIR /package_files/flops_manager

CMD ["poetry", "run", "python", "main.py"]
