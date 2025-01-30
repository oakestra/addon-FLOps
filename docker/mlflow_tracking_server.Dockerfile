FROM python:3.10-slim-buster
LABEL org.opencontainers.image.source=https://github.com/oakestra/addon-flops

# To be able to use MySQL for MLflow we need to install multiple Python dependencies.
RUN pip install \
        mlflow==2.18.0 \
        pymysql==1.1.0 \
        cryptography==42.0.7

# TODO(malyuka): Turn back to 7027 - once the networking bug is fixed
ENV TRACKING_SERVER_PORT=5000
EXPOSE $TRACKING_SERVER_PORT
