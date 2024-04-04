FROM python:3.12-slim

ARG NEXUS=nexus.svrw.oao.rzd

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update &&

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .