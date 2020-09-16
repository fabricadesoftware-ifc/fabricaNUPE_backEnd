FROM node:14.11-alpine3.10
LABEL mantainer="Luis Guerreiro <luiscvlh11@gmail.com>"

WORKDIR /usr/nupe

COPY nupe_frontend /usr/nupe
RUN npm install && npm run build
