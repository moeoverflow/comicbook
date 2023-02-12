FROM python:3.10-slim-buster

WORKDIR /usr/src/app

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv sync

COPY . .
