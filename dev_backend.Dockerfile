FROM python:3.6-slim-buster
LABEL mantainer="Luis Guerreiro <luiscvlh11@gmail.com>"

WORKDIR /usr/nupe

ENV SECRET_KEY=justasomekeytocandevelop \
    DEBUG=True \
    # superuser
    DJANGO_SUPERUSER_EMAIL=nupexample@example.com \
    DJANGO_SUPERUSER_PASSWORD=nuperoot \
    # db
    DATABASE_URL=postgres://nupe:nupe@db:5432/nupe

# build-essential para utilizar o "make" do sphinx
RUN apt-get update && apt-get install git build-essential -y && \
    pip3 install poetry==1.0.5 && \
    poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml /usr/nupe/
RUN poetry install --no-root

# instala os git hooks
COPY .pre-commit-config.yaml /usr/nupe
COPY .git /usr/nupe/.git
RUN pre-commit install -t pre-commit -t pre-push

COPY nupe /usr/nupe/nupe
RUN poetry install
