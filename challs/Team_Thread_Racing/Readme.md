# Team Thread Racing (by VrumVrum)

## Exploit

There is a race condition in the server code. If we send 0x133c0de and then 0xdeadc0de we can abuse race condition to print the flag.
Solution uses brute force approach.

## Compile

`gcc -o app server.c -pthread`

## Flag

Locally I receive the flag within 3-5 seconds: `DCTF{ButCanYouWinAgain?}`
