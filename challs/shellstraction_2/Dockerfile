FROM ubuntu:18.04

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get -y update && \
    apt-get -y install socat coreutils build-essential && \
    apt-get -y install python3 

COPY chall/flag.txt /
COPY handle_conn.py /
COPY chall/app.c /

RUN gcc -fstack-protector -o app app.c && \
    rm -f app.c && \
    chmod 555 /app && \
    chmod 444 /flag.txt

EXPOSE 1337

CMD socat -T 30 \
    TCP-LISTEN:1337,nodelay,reuseaddr,fork \
    EXEC:"python3 handle_conn.py"