FROM python:3.8-slim

RUN apt-get update
RUN apt-get -y install cron

RUN mkdir /app
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app
