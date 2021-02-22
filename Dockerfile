ARG PYTHON_VER

FROM python:${PYTHON_VER}-slim

RUN pip install --upgrade pip \
  && pip install poetry

WORKDIR /local
COPY . /local

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

RUN pip install /local/packages/pynautobot-1.0.0.tar.gz
