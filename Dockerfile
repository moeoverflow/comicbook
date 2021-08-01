FROM python:3.9-slim-buster

WORKDIR /usr/src/app

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv sync

COPY . .

EXPOSE 8080
CMD pipenv run gunicorn --worker-class eventlet -w 1 --threads 12 -b 0.0.0.0:8080 webapp:app
