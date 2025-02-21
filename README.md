# PythonLab

python thirty party library learning and note.

## setup developing environment

Install [pyenv](https://github.com/pyenv/pyenv) and [uv](https://docs.astral.sh/uv/getting-started/installation/).

## Docker note

``dockerfile
# Base image
FROM python:3.12 as build

RUN apt-get update && apt-get install -y build-essential curl
ENV VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip uv

COPY ./requirements.txt .
RUN python -m uv venv /opt/venv && \
    python -m uv pip install --no-cache -r requirements.txt

# App image
FROM python:3.12-slim-bookworm
COPY --from=build /opt/venv /opt/venv

# Activate the virtualenv in the container
# See here for more information:
# https://pythonspeed.com/articles/multi-stage-docker-python/
ENV PATH="/opt/venv/bin:$PATH"
```
