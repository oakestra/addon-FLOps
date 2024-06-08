FROM python:3.10-slim

COPY pyproject.toml pyproject.toml
RUN pip install poetry~=1.8.2 && poetry lock && poetry install --no-root

WORKDIR /mock_data_provider
COPY mock_data_provider /mock_data_provider
RUN poetry install

RUN poetry add git+https://github.com/Malyuk-A/tmp_flops_utils.git@main

ENV ML_DATA_SERVER_COMMUNICATION_CHANNEL_PORT=11027
EXPOSE $ML_DATA_SERVER_COMMUNICATION_CHANNEL_PORT
