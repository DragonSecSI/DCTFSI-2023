FROM node:latest

ENV NODE_ENV production

WORKDIR /app

COPY package*.json ./

RUN npm install

ARG FLAG
ENV FLAG ${FLAG}
ARG HOST
ENV HOST ${HOST}
ARG FQDN
ENV FQDN ${FQDN}

COPY src/ ./src

RUN groupadd nodeuser && useradd -g nodeuser nodeuser && chown -R nodeuser:nodeuser /app

USER nodeuser

CMD ["node", "src/index.js"]