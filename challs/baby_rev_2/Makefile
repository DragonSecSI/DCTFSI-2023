.PHONY: default build clean

default := build

build: main.c shellcode.s build.py flag.txt
	chmod u+x build.py
	./build.py

clean:
	-rm baby_rev_2 baby_rev.tar.gz

test: build
	./baby_rev_2 < flag.txt

dist: build
	tar -czvf baby_rev_2.tar.gz baby_rev_2
