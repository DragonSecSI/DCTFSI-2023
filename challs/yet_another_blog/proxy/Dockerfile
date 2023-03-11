FROM nginx:latest

COPY nginx.conf /tmp/nginx.conf

ARG FQDN
ENV FQDN ${FQDN}

RUN envsubst '${FQDN}' < /tmp/nginx.conf > /etc/nginx/conf.d/nginx.conf
