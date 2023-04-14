FROM ubuntu:18.04@sha256:8da4e9509bfe5e09df6502e7a8e93c63e4d0d9dbaa9f92d7d767f96d6c20a78a


RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get -y update && \
    apt-get -y install socat coreutils build-essential locales
    
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8 

RUN apt-get -y install python3 python3-pip python3-dev libssl-dev libffi-dev

# nano tmux and ruby
RUN apt-get -y install nano tmux ruby

# gdb and git
RUN apt-get -y install gdb git

# pwndbg
RUN git clone https://github.com/pwndbg/pwndbg && \
    cd pwndbg && \
    ./setup.sh && \
    cd ..

# pwntools
RUN python3 -m pip install -U pip && \
    python3 -m pip install -U pwntools && \
    python3 -m pip install -U ROPgadget

# onegadget
RUN gem install one_gadget

COPY chall/* /
COPY sol.py /
COPY ld.so /
COPY libc.so /
COPY Makefile /
COPY patchelf /

#RUN gcc -fno-stack-protector -no-pie -o bof_2 main.c && \
RUN chmod 555 /app && \
    chmod 444 /flag.txt

EXPOSE 1337

CMD socat -T 30 \
    TCP-LISTEN:1337,nodelay,reuseaddr,fork \
    EXEC:"stdbuf -i0 -o0 -e0 ./app"
