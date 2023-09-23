FROM python:3.11.5-slim

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN pip install poetry==1.6.1
RUN poetry config virtualenvs.create false
RUN poetry install --only main --no-interaction --no-ansi

# Maybe you wanna copy resources inside project
# COPY ./resources ./resources

COPY ./src ./src

WORKDIR /app/src