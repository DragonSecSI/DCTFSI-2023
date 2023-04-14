default:
	gcc -o app app.c
	chmod +x app

mod:
	gcc -Xlinker -rpath=. -Xlinker -I/ld.so -o app app.c
	chmod +x app

