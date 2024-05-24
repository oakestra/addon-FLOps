FROM python:3.10-slim

COPY pyproject.toml pyproject.toml
RUN pip install poetry~=1.8.2 && poetry lock && poetry install --no-root

WORKDIR /ml_data_server
COPY ml_data_server /ml_data_server
RUN poetry install

# TRUE for verbose logging
ENV FLASK_ENV=development
ENV FLASK_DEBUG=TRUE

ENV ML_DATA_SERVER_PORT=11027
EXPOSE $ML_DATA_SERVER_PORT

RUN poetry add git+https://github.com/Malyuk-A/tmp_flops_utils.git@main

CMD ["poetry", "run", "python", "main.py"]
