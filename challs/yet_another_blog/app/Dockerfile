FROM node:18-alpine

WORKDIR /app

RUN mkdir /.npm

COPY package*.json ./

RUN npm install

ENV NODE_ENV=production
ENV FLAG="DCTF{ju5t_upgr4d3_j50nw3b70k3n_t0_m0r3_th4n_8.5.1_9a042926a}"
ENV HOST="0.0.0.0"

COPY src/ ./src

CMD ["node", "src/index.js"]
