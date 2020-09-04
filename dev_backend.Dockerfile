FROM python:3.6-slim-buster
LABEL mantainer="Luis Guerreiro <luiscvlh11@gmail.com>"

WORKDIR /usr/nupe

ENV DEBUG=True \
    MEDIA_ROOT=media/test \
    MEDIA_URL=/media/test/

# build-essential para utilizar o "make" do sphinx
RUN apt-get update && apt-get install git build-essential -y && \
    pip3 install poetry==1.0.5 && \
    poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml /usr/nupe/
RUN poetry install --no-root

COPY nupe /usr/nupe/nupe
RUN poetry install
