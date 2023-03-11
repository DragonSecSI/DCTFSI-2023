FROM ubuntu:20.04

EXPOSE 1337

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get -y update && \
    apt-get -y install python3

COPY chall/flag.txt /
COPY chall/app /
COPY chall/serve.py /

RUN chmod 555 /serve.py && \
    chmod 444 /flag.txt

CMD python3 /serve.py
