#define _GNU_SOURCE
#define __STDC_WANT_LIB_EXT1__ 1
#include <stdlib.h>
#include <stdio.h>
#include <sys/mman.h>
#include <string.h>

const char SHELLCODE[] = "<shellcode>";

int main(int argc, char *argv)
{
    puts("What is the flag?");
    char inp[64];
    fgets(inp, sizeof inp, stdin);
    inp[strcspn(inp, "\n")] = 0;

    void *mem = mmap(NULL, sizeof(SHELLCODE), PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE | MAP_ANON, 0, 0);
    memcpy(mem, SHELLCODE, sizeof(SHELLCODE));

    if (!((int (*)(char *))mem)(inp))
    {
        puts("Correct! You got the flag!");
    }
    else
    {
        puts("Try again...");
    }
}
