FROM node:18-alpine

WORKDIR /app

RUN mkdir /.npm

COPY package*.json ./

RUN npm install

ENV NODE_ENV production
ARG FLAG
ENV FLAG ${FLAG}
ARG HOST
ENV HOST ${HOST}

COPY src/ ./src

RUN addgroup nodeuser && adduser -DG nodeuser nodeuser && chown -R nodeuser:nodeuser /app /.npm
USER nodeuser

CMD ["node", "src/index.js"]