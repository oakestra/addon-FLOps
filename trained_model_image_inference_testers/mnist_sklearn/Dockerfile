FROM python:3.10-slim

COPY pyproject.toml pyproject.toml
RUN pip install poetry~=1.8.2 && poetry lock && poetry install --no-root

WORKDIR /inference_tester
COPY inference_tester /inference_tester
RUN poetry install

RUN poetry add git+https://github.com/Malyuk-A/tmp_flops_utils.git@main

CMD poetry run python main.py
