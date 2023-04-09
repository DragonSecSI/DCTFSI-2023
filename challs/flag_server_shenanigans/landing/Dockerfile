FROM python:alpine AS builder

WORKDIR /app

COPY . ./

# Set environment variables
ARG WIFI_COORDS

RUN python build.py

FROM nginx:alpine

COPY --from=builder /app/index.html /usr/share/nginx/html/index.html
