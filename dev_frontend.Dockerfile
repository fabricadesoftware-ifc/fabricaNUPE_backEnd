FROM node:14.11-alpine3.10
LABEL mantainer="Luis Guerreiro <luiscvlh11@gmail.com>"

WORKDIR /usr/nupe

ENV API_URL=http://localhost/ \
    NUXT_MODE=spa

RUN apt-get update && apt-get install git -y

COPY nupe_frontend /usr/nupe
RUN npm install
