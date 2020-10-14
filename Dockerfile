FROM nvidia/cuda:11.1-cudnn8-devel-ubuntu18.04 as base

RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends \
  curl \
  wget \
  git \
  fish \
  make \
  build-essential \
  libssl-dev \
  zlib1g-dev \
  libbz2-dev \
  libreadline-dev \
  libsqlite3-dev \
  llvm \
  libncurses5-dev \
  xz-utils \
  tk-dev \
  libxml2-dev \
  libxmlsec1-dev \
  libffi-dev \
  liblzma-dev \
  && rm -rf /var/lib/apt/lists/*

FROM base as deps

WORKDIR /deps
COPY poetry.lock pyproject.toml /deps/

ENV PYTHON_VERSION=3.7.6 \
  POETRY_VERSION=1.1.2 \
  PATH="/root/.local/bin:/root/.pyenv/shims:/root/.pyenv/bin:$PATH"

RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash \
  && curl -fsSL https://starship.rs/install.sh | bash -s -- --yes \
  && curl https://pyenv.run | bash -s -- --yes \
  && pyenv install $PYTHON_VERSION \
  && pyenv global $PYTHON_VERSION \
  && python -m pip install --upgrade pip \
  && pip install "poetry==$POETRY_VERSION" \
  && python -m pip install --user pipx \
  && pipx install black \
  && pipx install dvc \
  && poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi
