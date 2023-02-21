FROM python:3.8.5-slim-buster

ENV GIT_PYTHON_REFRESH=quiet

ENV PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY . /app

WORKDIR /app

RUN pip install \
    --no-warn-script-location \
    --no-cache-dir \
    --upgrade \
    --disable-pip-version-check \
    -r /app/requirements.txt

RUN rm -rf /tmp/*

CMD ["python3", "-m", "meddoc"]