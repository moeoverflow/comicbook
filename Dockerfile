FROM python:3.7.6-slim-stretch

WORKDIR /usr/src/app

COPY requirements.txt .

RUN python -m pip install -r requirements.txt && \
    python -m pip install gunicorn && \
    python -m pip install eventlet

COPY . .

EXPOSE 8080
CMD gunicorn --worker-class eventlet -w 1 --threads 12 -b 0.0.0.0:8080 webapp:app
