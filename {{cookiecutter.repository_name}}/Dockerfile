FROM --platform=linux/amd64 ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS build_amd64

RUN apt-get update && apt-get install \
  --no-install-recommends -qq -y \
  curl \
  ca-certificates \
  build-essential \
  locales \
  locales-all \
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

# Configure locales
RUN sed -i -e 's/# \(pt_BR\.UTF-8 .*\)/\1/' /etc/locale.gen && locale-gen
ENV LANG=pt_BR.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=pt_BR.UTF-8

# Update pip and setuptools
RUN uv pip install --upgrade pip --system
RUN uv pip install --upgrade setuptools --system

WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Copy configs to install project
COPY uv.lock pyproject.toml README.md ./

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching

# Copy project
COPY ./{{cookiecutter.repository_name|lower|replace("-", "_")}} ./{{cookiecutter.repository_name|lower|replace("-", "_")}}

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []

# Remove unnecessary files
RUN rm -rf uv.lock pyproject.toml README.md
