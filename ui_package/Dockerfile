FROM python:3.10-slim
LABEL org.opencontainers.image.source https://github.com/oakestra/plugins-FLOps-UI

COPY pyproject.toml pyproject.toml
RUN pip install poetry~=1.8.2 && poetry lock && poetry install --no-root

WORKDIR /flops_ui
COPY flops_ui /flops_ui
RUN poetry install

ENV FLOPS_UI_PORT=2727
EXPOSE $FLOPS_UI_PORT
