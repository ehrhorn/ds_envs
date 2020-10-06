FROM python:3.7.6-slim-buster

ENV PIP_DISABLE_PIP_VERSION_CHECK=on \
  POETRY_VERSION=1.1.0 \
  PATH="/root/.local/bin:${PATH}"

RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -yq \
  curl \
  git \
  fish


RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash
RUN curl -fsSL https://starship.rs/install.sh | bash -s -- --yes
RUN pip install "poetry==$POETRY_VERSION"

RUN python -m pip install --user pipx
RUN pipx install black
RUN pipx install dvc

WORKDIR /deps
COPY poetry.lock pyproject.toml /deps/

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi
