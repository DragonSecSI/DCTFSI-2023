FROM php:8.0.3-apache

WORKDIR /var/www/html

ARG FLAG1
ENV FLAG1=$FLAG1

# Copy the source code
COPY *.php  ./
COPY api/*.php  ./api/
COPY *.css  ./

USER www-data