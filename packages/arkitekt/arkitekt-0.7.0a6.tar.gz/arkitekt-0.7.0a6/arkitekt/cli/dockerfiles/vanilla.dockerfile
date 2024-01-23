FROM python:3.8-slim-buster

RUN pip install "arkitekt[all]>=0.7.0a2"

RUN mkdir /app
WORKDIR /app
COPY .arkitekt /app/.arkitekt
COPY app.py /app/app.py
