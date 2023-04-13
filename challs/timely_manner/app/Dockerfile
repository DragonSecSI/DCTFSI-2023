FROM bhgedigital/envsubst AS build

WORKDIR /build

ARG FLAG    
ENV FLAG ${FLAG}

ARG REDIRECT_URL
ENV REDIRECT_URL ${REDIRECT_URL}

COPY index.php .
COPY flag.php /tmp/flag.php

RUN envsubst '${FLAG} ${REDIRECT_URL}' < /tmp/flag.php > ./flag.php

FROM php:7.1-apache

WORKDIR /var/www/html/

COPY --from=build /build/*.php .
