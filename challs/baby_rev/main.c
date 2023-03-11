#include <stdio.h>
#include <string.h>

const char FLAG[] = "<flag>";
const char KEY[] = "<key>";
unsigned int MAGIC = "<magic>";

void encrypt(char *pt)
{
    for (int i = sizeof(FLAG) - 1; i >= 0; i--)
    {
        pt[i] = ((pt[i] ^ KEY[i]) + MAGIC - i);
        MAGIC *= MAGIC;
    }
}

int check_flag(char *inp)
{
    encrypt(inp);
    return memcmp(inp, FLAG, sizeof(FLAG)) == 0;
}

int main(int argc, char *argv)
{
    puts("What is the flag?");
    char inp[64];
    fgets(inp, sizeof inp, stdin);
    inp[strcspn(inp, "\n")] = 0;
    if (strlen(inp) == sizeof(FLAG) && check_flag(inp))
    {
        puts("Correct! You got the flag!");
    }
    else
    {
        puts("Try again...");
    }
}
