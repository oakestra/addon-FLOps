FROM python:3.10-slim

COPY pyproject.toml pyproject.toml
RUN pip install poetry~=1.8.2 && poetry lock && poetry install --no-root

WORKDIR /data_manager
COPY data_manager /data_manager
RUN poetry install

# TRUE for verbose logging
ENV FLASK_ENV=development
ENV FLASK_DEBUG=TRUE

ENV DATA_MANAGER_PORT=11027
EXPOSE $DATA_MANAGER_PORT

CMD ["poetry", "run", "python", "main.py"]
