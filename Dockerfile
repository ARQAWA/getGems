FROM python:3.12

ENV PYTHONUNBUFFERED 1

RUN apt-get update -y && \
    apt-get upgrade -y && \
    pip install -U pip

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
