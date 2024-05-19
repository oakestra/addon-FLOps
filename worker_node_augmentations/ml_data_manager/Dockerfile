FROM python:3.10-slim-buster
LABEL org.opencontainers.image.source https://github.com/oakestra/oakestra

ADD requirements.txt /
RUN pip install -r requirements.txt
ADD . /

ENV FLASK_ENV=development
ENV FLASK_DEBUG=TRUE

ENV ML_DATA_MANAGER_PORT=11027
EXPOSE $ML_DATA_MANAGER_PORT

CMD ["python", "ml_data_manager.py"]
