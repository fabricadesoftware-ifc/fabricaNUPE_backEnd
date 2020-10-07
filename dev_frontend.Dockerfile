FROM node:14.11-alpine3.10
LABEL maintainer="Luis Guerreiro <luiscvlh11@gmail.com>"

WORKDIR /usr/nupe_frontend

ENV API_URL=http://localhost:8000/ \
    NUXT_MODE=spa

RUN apk add --no-cache git

COPY nupe_frontend /usr/nupe_frontend
RUN npm install
