FROM python:3.10-slim

COPY pyproject.toml pyproject.toml
RUN pip install poetry~=1.8.2 && poetry lock && poetry install --no-root

WORKDIR /project_observer
COPY project_observer /project_observer
RUN poetry install

RUN poetry add git+https://github.com/Malyuk-A/tmp_flops_utils.git@main

ENV PROJECT_OBSERVER_PORT=2727
EXPOSE $PROJECT_OBSERVER_PORT
