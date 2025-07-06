# Dockerfile
FROM python:3.9-slim-buster

WORKDIR /app

RUN pip install redis celery celeryviz

COPY . .
CMD ["celery", "-A", "example_app", "worker", "--loglevel=info", "-E"]