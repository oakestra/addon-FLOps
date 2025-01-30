FROM python:3.10-slim

COPY pyproject.toml pyproject.toml
RUN pip install poetry~=1.8.2 && poetry lock && poetry install --no-root

# https://github.com/python-poetry/poetry/issues/1573#issuecomment-1889151744
RUN mkdir -p /root/.cache/pypoetry/virtualenvs

WORKDIR /inference_tester
COPY inference_tester /inference_tester
RUN poetry install

RUN poetry add git+https://github.com/oakestra/addon-FLOps.git@main#subdirectory=utils_library

ENTRYPOINT ["poetry", "run", "python", "main.py"]
