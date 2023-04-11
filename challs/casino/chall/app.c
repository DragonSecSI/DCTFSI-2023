#include <stdio.h>
#include <stdlib.h>
#include <sys/random.h>

int balance = 100;
const int cap = 10000;
const int rounds = 10;

int main()
{
	puts("Welcome to DCTF casino!");

	for (int round = 0; round < rounds; round++)
	{
		printf("Round %d/%d, you have %d Eur in your account.\n", round + 1, rounds, balance);
		printf("How much do you want to bet? ");

		int bet;
		scanf("%d", &bet);

		if (bet > balance)
		{
			puts("You don't have that much money!");
			return 1;
		}

		int random;
		getrandom(&random, 1, 0);
		random = random % 10;
		int guess;
		puts("Guess a number between 0 and 9: ");
		scanf("%d", &guess);

		if (guess == random)
		{
			puts("You won!");
			balance += bet;
		}
		else
		{
			puts("You lost!");
			balance -= bet;
		}

		if (balance == 0)
		{
			puts("You lost all your money!");
			return 1;
		}
		else if (balance >= cap)
		{
			puts("Wow, you're rich now!");

			FILE *f = fopen("flag.txt", "r");
			char flag[100];
			fgets(flag, 100, f);
			printf("Here's your flag: %s", flag);

			return 0;
		}
	}

	puts("This was nice, wasn't it? Let's play again soon!");
	return 0;
}
