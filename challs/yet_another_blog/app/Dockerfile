FROM node:latest

WORKDIR /app

ARG FLAG
ENV FLAG ${FLAG}
ARG HOST
ENV HOST ${HOST}

COPY package*.json ./

RUN npm install

RUN groupadd nodeuser && useradd -g nodeuser nodeuser 

COPY src/ ./src

ENV NODE_ENV production

USER nodeuser

CMD ["node", "src/index.js"]