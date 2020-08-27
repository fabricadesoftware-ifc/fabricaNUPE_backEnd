FROM python:3.8-slim-buster
LABEL mantainer="Luis Guerreiro <luiscvlh11@gmail.com>"

WORKDIR /usr/nupe

RUN pip3 install poetry==1.0.5 && \
    poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml /usr/nupe/
RUN poetry install --no-root

COPY nupe /usr/nupe/nupe
RUN poetry install
