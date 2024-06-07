FROM python:3.10-slim-buster

# To be able to use MySQL for MLflow we need to install multiple python dependencies.
RUN pip install \
        mlflow==2.12.1 \
        pymysql==1.1.0 \
        cryptography==42.0.7

ENV TRACKING_SERVER_PORT=9027
EXPOSE $TRACKING_SERVER_PORT
