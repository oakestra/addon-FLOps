FROM python:3.10-slim
LABEL org.opencontainers.image.source=https://github.com/oakestra/addon-flops

COPY pyproject.toml pyproject.toml
RUN pip install poetry~=1.8.2 && poetry lock && poetry install --no-root

WORKDIR /project_observer
COPY project_observer /project_observer
RUN poetry install

RUN poetry add git+https://github.com/oakestra/addon-FLOps.git@main#subdirectory=utils_library

ENV PROJECT_OBSERVER_PORT=2727
EXPOSE $PROJECT_OBSERVER_PORT
