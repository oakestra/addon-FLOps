FROM python:3.10-slim

COPY pyproject.toml pyproject.toml
RUN pip install poetry~=1.8.2 && poetry lock && poetry install --no-root

WORKDIR /inference_tester
COPY inference_tester /inference_tester
RUN poetry install

RUN poetry add git+https://github.com/oakestra/addon-FLOps.git@main#subdirectory=utils_library

CMD poetry run python main.py
