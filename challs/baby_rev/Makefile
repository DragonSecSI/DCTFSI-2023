.PHONY: default build clean

default := build

build: main.c gen_flag.py flag.txt
	chmod u+x gen_flag.py
	./gen_flag.py
	gcc main_compile.c -s -O2 -o baby_rev

clean:
	-rm baby_rev main_compile.c baby_rev.tar.gz

test: build
	./baby_rev < flag.txt

dist: build
	tar -czvf baby_rev.tar.gz baby_rev
