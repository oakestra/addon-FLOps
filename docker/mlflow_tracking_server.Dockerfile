FROM python:3.10-slim-buster
LABEL org.opencontainers.image.source https://github.com/oakestra/oakestra

RUN pip install mlflow==2.12.1 &&\
    # Note: For now we use a simply serverless sqlite DB for the mlflow backend server.
    # This can be replaced by a dedicated remote DB (e.g. Postgres, etc.)
    # Note: MongoDB is not natively supported by mlflow. There seems to be user-created plugins though.
    apt-get update && apt-get install sqlite3 && apt-get clean && sqlite3 mlflow_backend_store.db
ENV TRACKING_SERVER_PORT=7027

CMD bash -c 'mlflow server --backend-store-uri sqlite:////mlflow_backend_store.db --host 0.0.0.0 --port ${TRACKING_SERVER_PORT}'
# TODO add ~ --default-artifact-root s3://${AWS_BUCKET}/artifacts
