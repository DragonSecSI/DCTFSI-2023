FROM php:8.0.3-apache

WORKDIR /var/www/html

ENV FLAG1="DCTF{c4r3fu1_w1th_c0mm3nts_33e9c9d80ed}"

# Copy the source code
COPY *.php  ./
COPY api/*.php  ./api/
COPY *.css  ./

RUN sed -i 's/Listen 80/Listen 8000/' /etc/apache2/ports.conf

USER www-data
