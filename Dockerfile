FROM python:3.10-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN apk add --no-cache bash
COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .
COPY .env.dev .env
