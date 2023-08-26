FROM python:3.11.3-slim-bullseye

WORKDIR /app

COPY ./resources ./resources

COPY ./src ./src

COPY ./requirements.txt /app/

RUN pip install -r requirements.txt

RUN rm requirements.txt