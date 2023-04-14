#include <stdio.h>
#include <stdlib.h>
#include <string.h>


char* kids[10];
// char* allowance;


void setup() {
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);
    setvbuf(stderr, 0, _IONBF, 0);
}

void welcome() {
    char buf[30];

    printf("Enter your name please: ");
    fgets(buf, 30, stdin);
    printf("Welcome to the D-Money Parenting Simulator ");
    printf(buf);
    printf("!\n");
}

void menu() {
    puts("");
    puts("Here is what we offer:");
    puts("1 Allocate allowance");
    puts("2 View allowance");
    puts("3 Cancel allowance");
    puts("4 Quit");
}

void read_int(int* num) {
    char buf[3];
    int c;
    
    printf("> ");
    // scanf("%d", num);
    // getc(stdin);

    fgets(buf, 3, stdin);

    if (buf[strlen(buf) - 1] == '\n') {
        // already read \n
        buf[strlen(buf) - 1] = '\0';
    }
    else {
        // didn't real \n yet, read until \n
        while ((c = getc(stdin)) != '\n') {;}
    }
    *num = (int) strtol(buf, NULL, 10);
}

void read_str(char* buf) {
    int c;

    printf("> ");
    fgets(buf, 30, stdin);

    if (buf[strlen(buf) - 1] == '\n') {
        buf[strlen(buf) - 1] = '\0';
    }
    else {
        // didn't real \n yet, read until \n
        while ((c = getc(stdin)) != '\n') {;}
    }
}

int select_kid() {
    int kid = -1;

    puts("Which kid would you like to select?");
    read_int(&kid);
    printf("Selected kid %d\n", kid);
    if (kid > 9 || kid < 0) {
        puts("You don't have that many kids.");
        return -1;
    }
    return kid;
}

void allocate_allowance() {
    int kid = select_kid();
    int money = 0;

    if (kid < 0) return;

    // can create dangling pointers
    kids[kid] = malloc(30);
    if (kids[kid] == NULL) {
        fprintf(stderr, "malloc error\n");
        return;
    }

    puts("How much money would you like to allocate your kid to?");
    read_str(kids[kid]);
    // fgets ends reading when reaching N - 1, \n or EOF. It stores the last char read (including \n or EOF) and appends \0.
    // kids[kid][strlen(kids[kid]) - 1] = '\0';
    puts("Money allocated successfully.");
}

void cancel_allowance() {
    int kid = select_kid();
    if (kid < 0) return;

    if (kids[kid] == NULL) {
        puts("You didn't even give them any money!");
        return;
    }
    free(kids[kid]);
    puts("Allowance cancelled.");
}

void view_allowance() {
    int kid = select_kid();
    if (kid < 0) return;

    if (kids[kid] == NULL) {
        puts("You didn't give them any money!");
        return;
    }

    printf("You have allocated $%s to kid %d.\n", kids[kid], kid);
}

void sim() {
    int decision = 0;

    while (1) {
        menu();
        read_int(&decision);
        
        switch (decision) {
            case 1:
                allocate_allowance();
                break;
            case 2:
                view_allowance();
                break;
            case 3:
                cancel_allowance();
                break;
            case 4:
                puts("Goodbye!");
                return;
            default:
                puts("Invalid input!");
                break;
        }
    }
}

int main() {

    setup();
    welcome();
    sim();

    return 0;
}