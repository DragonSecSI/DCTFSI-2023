FROM python:3

RUN apt-get -y update && \
    apt-get install -y socat coreutils && \
    rm -rf /var/lib/apt/lists/*

COPY ./chall /

RUN chmod 444 /secret.py && \
    chmod 555 /xoxo.py && \
    chmod 555 /xoxo.sh

ENTRYPOINT []
CMD socat -T 30 \
    TCP-LISTEN:1337,nodelay,reuseaddr,fork \
    EXEC:"stdbuf -i0 -o0 -e0 /xoxo.sh"

EXPOSE 1337
