FROM python:3.7

WORKDIR /app

ENV FLAG="DCTF{r54_g0e5_l4l4l4_fa44d37}"

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt


RUN apt-get -y update && \
    apt-get -y install socat coreutils

COPY app.py .

RUN chmod 555 /app/app.py

EXPOSE 1337

CMD socat -T 30 \
    TCP-LISTEN:1337,nodelay,reuseaddr,fork \
    EXEC:"stdbuf -i0 -o0 -e0 python /app/app.py"
