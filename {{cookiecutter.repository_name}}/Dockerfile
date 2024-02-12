FROM python:3.11.3-slim-bullseye

RUN apt-get update && apt-get install \
		--no-install-recommends -qq -y \
  build-essential \
  locales \
  git \
  python3-pip \
  python3-setuptools \
  gcc \
  g++ \
  libpoppler-cpp-dev \
  poppler-utils \
  pkg-config \
  cmake \
  python3-opencv \
  libopencv-dev \
  libjpeg-dev \ 
  libpng-dev

# configura locales
RUN sed -i -e 's/# \(pt_BR\.UTF-8 .*\)/\1/' /etc/locale.gen && locale-gen
ENV LANG pt_BR.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL pt_BR.UTF-8
RUN apt-get install -y locales locales-all

WORKDIR /app

# instala os requerimentos do projeto
COPY poetry.lock pyproject.toml /app/

RUN pip install poetry==1.6.1
RUN poetry config virtualenvs.create false
RUN poetry install --only main --no-interaction --no-ansi

# copia o diretório do projeto
COPY ./{{cookiecutter.project_name}} ./{{cookiecutter.project_name}}

# limpa arquivos desnecessários
RUN rm -rf poetry.lock pyproject.toml
