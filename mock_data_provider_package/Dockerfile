FROM python:3.10-slim

COPY pyproject.toml pyproject.toml
RUN pip install poetry~=1.8.2 && poetry lock && poetry install --no-root

WORKDIR /mock_data_provider
COPY mock_data_provider /mock_data_provider
RUN poetry install

CMD ["poetry", "run", "python", "main.py"]
