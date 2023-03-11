FROM bhgedigital/envsubst AS build

WORKDIR /build

ENV FLAG="DCTF{1t5_4ll_4b0ut_7h3_p53udo_r4nd0m_numb3r5_424e7f9234}"

ENV REDIRECT_URL="https://tmnt.dctf.si/"

COPY index.php .
COPY flag.php /tmp/flag.php

RUN envsubst '${FLAG} ${REDIRECT_URL}' < /tmp/flag.php > ./flag.php

FROM php:7.1-apache

WORKDIR /var/www/html/

RUN sed -i 's/Listen 80/Listen 8000/' /etc/apache2/ports.conf

COPY --from=build /build/*.php .
