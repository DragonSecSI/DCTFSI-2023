#include <stdio.h>
#include <stdlib.h>

#define int unsigned int

const int N = 0xc0;

void win() {
	system("/bin/sh");
}

void swap(int *a, int *b) {
	if(*a < *b) {
		*a += *b;
		*b = *a - *b;
		*a = *a - *b;
	}
}

int gcd(int a, int b) {
	if(a == 0 || b == 0) {
		return a + b;
	} else {
		return gcd(b, a % b);			
	}	
}

int lcm(int a, int b) {
	swap(&a, &b);
	return (a * b) / gcd(a, b);
}

signed main() {

		int a, b;

		int n;

		printf("Input: ");
		scanf("%d", &n);

		int dp[1317][3193];

	for(int i = 0; i < n; i++) {
		scanf("%d%d", &a, &b);
		printf("%d\n", dp[a][b] = lcm(a, b));
	}
}