FROM python:3.10-slim-buster
LABEL org.opencontainers.image.source https://github.com/oakestra/oakestra

RUN apt-get update && apt-get install git wget libnss3-tools -y && apt-get clean

RUN wget https://github.com/FiloSottile/mkcert/releases/download/v1.4.4/mkcert-v1.4.4-linux-amd64 &&\
    mv mkcert-v1.4.4-linux-amd64 /usr/bin/mkcert &&\
    chmod +x /usr/bin/mkcert

ADD requirements.txt /

RUN pip install -r requirements.txt

ADD . /

# TRUE for verbose logging
ENV FLASK_ENV=development
ENV FLASK_DEBUG=TRUE

ENV ROOT_FL_IMAGE_REGISTRY_PORT=5073
ENV ROOT_FL_MANAGER_PORT=5072
EXPOSE $ROOT_FL_MANAGER_PORT

ENV ROOT_FL_MQTT_BROKER_URL=9027
ENV ROOT_FL_MQTT_BROKER_URL=root_fl_mqtt

ENV CAROOT=/etc/ssl

CMD ["python", "root_fl_manager.py"]
