# pull official base image
FROM python:3.12-alpine

# set work directory
WORKDIR /usr/src/backend

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements file
COPY ./requirements.txt /usr/src/backend/requirements.txt

# install dependencies
RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
    openssl-dev libffi-dev gcc musl-dev python3-dev \
    postgresql-dev bash \
    && pip install --upgrade pip setuptools wheel \
    && pip install -r /usr/src/backend/requirements.txt \
    && rm -rf /root/.cache/pip

# copy project
COPY . /usr/src/backend/