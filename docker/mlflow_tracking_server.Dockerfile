FROM python:3.10-slim-buster
LABEL org.opencontainers.image.source https://github.com/oakestra/oakestra

# To be able to use MySQL for MLflow we need to install multiple python dependencies.
RUN pip install mlflow==2.12.1 pymysql==1.1.0 cryptography==42.0.7
ENV TRACKING_SERVER_PORT=7027


#CMD bash -c 'mlflow server --backend-store-uri sqlite:////mlflow_backend_store.db --host 0.0.0.0 --port ${TRACKING_SERVER_PORT} --serve-artifacts --artifacts-destination ftp://flops:flops@192.168.178.44/flops_artifacts'

# https://mlflow.org/docs/latest/tracking/backend-stores.html#supported-store-types
CMD bash -c 'mlflow server --backend-store-uri mysql+pymysql://root:oakestra@192.168.178.44:3306/mysql --host 0.0.0.0 --port ${TRACKING_SERVER_PORT} --serve-artifacts --artifacts-destination ftp://flops:flops@192.168.178.44/flops_artifacts'
