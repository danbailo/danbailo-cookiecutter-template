FROM python:3.11.3-slim-bullseye

WORKDIR /app

COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

# Maybe you wanna copy resources inside project
COPY ./resources ./resources

COPY ./src ./src

RUN rm requirements.txt