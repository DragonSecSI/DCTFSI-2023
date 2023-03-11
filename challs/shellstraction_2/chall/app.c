#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>
#include <ctype.h>
#include <errno.h>
#include <limits.h>
#include <dirent.h>
#include <fcntl.h>
#include <sys/file.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include <sys/types.h>


#define pf(format, ...);                fprintf(stdout, (format), ##__VA_ARGS__); fflush(NULL);
#define pfc(format, retval, ...);       fprintf(stdout, (format), ##__VA_ARGS__); fflush(NULL); lastex = retval;
#define perrorfc(str, errcode);         perror(str); lastex = errcode;
#define pc(format, retval, ...);        fprintf(stdout, (format), ##__VA_ARGS__); lastex = retval;
#define fc(retval);                     fflush(NULL); lastex = retval;
#define freenull(ptr);                  free(ptr); ptr = NULL;



char* user;
char* host;
char path[200];

int guard = 0;

char* notes_arr[10];

int token_count;
char* tokens[50];
char* sh_name;
int statp;
int background = 0;
int lastex = 0;

void process(int s) {
    switch (s) {
        case 17:
            wait(&statp);
            return;
    }
}

void setup() {
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);
    setvbuf(stderr, 0, _IONBF, 0);
}

void tokenize(char* line) {
    token_count = 0;
    int newtoken = 1;
    int multitoken = 0;
    if (line[0] == '#') {
        return;
    }
    int len = strlen(line);
    for (int i = 0; i < len; i++) {
        char curr = line[i];
        if (newtoken == 1) {
            if (token_count > 50) {
                puts("Too many tokens.");
                fflush(stdout);
                return;
            }

            if (isspace(curr) != 0) {
                line[i] = '\0';
                continue;
            }
            if (curr == '"') {
                multitoken = 1;
                tokens[token_count] = &(line[i+1]);
            }
            else {
                multitoken = 0;
                tokens[token_count] = &(line[i]);
            }
            newtoken = 0;

            token_count++;
            continue;
        }
        if ((multitoken == 1 && curr == '"') || (multitoken == 0 && isspace(curr))) {
            line[i] = '\0';
            newtoken = 1;
        }
    }
}

void name() {
    if (token_count == 1) {
        pf("%s\n", sh_name);
    } else {
        strncpy(sh_name, tokens[1], 100);
    }
    lastex = 0;
}

void help() {
    pfc("Help me!\n", 0);
}

void whoami() {
    pfc("%s\n", 0, user);
}

void hostname() {
    pfc("%s\n", 0, host);
}

void eton() {
    int index = -1;

    if (!guard) {
        pfc("Not enough memory available.", -1);
        return;
    }

    if (token_count < 2) {
        pfc("Not enough arguments for command note", 0);
        return;
    }

    if (strcmp(tokens[1], "help") == 0) {
        pf("This is a simple shell program for saving personal notes!");
    }
    else if (strcmp(tokens[1], "add") == 0) {
        if (token_count < 5) {
            pfc("Not enough arguments for command note", 0);
            return;
        }

        index = atoi(tokens[2]);
        if (index < 0 || index > 9) {
            pfc("Invalid note index!", 0);
            return;
        }

        int size = atoi(tokens[3]);
        if (size < 1) {
            pfc("Invalid note size.", 0);
            return;
        }

        pf("Creating a note...");
        notes_arr[index] = (char*) malloc(size);
        if (notes_arr[index] != NULL) {
            strncpy(notes_arr[index], tokens[4], strlen(tokens[4]));
        }
        pf("Note created");
    }
    else if (strcmp(tokens[1], "remove") == 0) {
        if (token_count < 3) {
            pfc("Not enough arguments for command note", 0);
            return;
        }
        
        pf("Removing notes...");

        index = atoi(tokens[2]);
        if (index < 0 || index > 9) {
            pfc("Invalid note index!", 0);
            return;
        }

        if (notes_arr[index] == NULL) {
            pfc("No note to remove.", 0);
            return;
        }

        free(notes_arr[index]);
        pf("Notes removed.");
    }
    else if (strcmp(tokens[1], "show") == 0) {
        if (token_count < 3) {
            pfc("Not enough arguments for command note", 0);
            return;
        }

        index = atoi(tokens[2]);
        if (index < 0 || index > 9) {
            pfc("Invalid note index!", 0);
            return;
        }

        if (notes_arr[index] == NULL) {
            pfc("No note to show.", 0);
            return;
        }

        pf("%s\n", notes_arr[index]);
    }
    else {
        pf("Invalid argument for command note");
    }

    lastex = 0;
}

void exit_shell() {
    int exit_code = 0;
    if (token_count == 1) {
        exit(exit_code);
    } else {
        exit_code = (int) strtol(tokens[1], NULL, 10);
        if (exit_code == INT_MIN || exit_code == INT_MAX) {
            perrorfc("strtol", errno);
            return;
        }
        
        exit(exit_code);
    }
}

void status() {
    pfc("%d\n", 0, lastex);
}

void print() {
    if (token_count > 1) {
        pf("%s", tokens[1]);
    }
    for (int i = 2; i < token_count; i++) {
        pf(" %s", tokens[i]);
    }
    fc(0);
}

void echo() {
    print();
    pfc("\n", 0);
}

void dirchange() {
    int out = 0;
    if (token_count == 1) {
        out = chdir("/");
    } else {
        out = chdir(tokens[1]);   
    }
    if (out != 0) {
        perrorfc("cd", errno);
    } else if (getcwd(path, sizeof(path)) == NULL) {
        perrorfc("dirchange", errno);
    } else {
        lastex = out;
    }
}

void dirwhere() {
    if (getcwd(path, sizeof(path)) != NULL) {
        pfc("%s\n", 0, path);
    } else {
        perrorfc("pwd", errno);
    }
}

void dirmake() {
    int out = mkdir(tokens[1], 0755);
    if (out != 0) {
        perrorfc("mkdir", errno);
    }
    else lastex = 0;
}

void dirlist() {
    struct dirent *entry;
    DIR *dir;
    if (token_count == 1) {
        char cwd[200];
        if (getcwd(cwd, sizeof(cwd)) == NULL) {
            perrorfc("ls", errno);
            return;
        }
        dir = opendir(cwd);
    }
    else {
        dir = opendir(tokens[1]);
    }

    if (dir == NULL) {
        perrorfc("ls", errno);
        return;
    }

    char* dirs[100];
    int counter = 0;
    while ((entry = readdir(dir)) != NULL) {
        char* nm = (entry->d_name);
        dirs[counter++] = nm;
    }
    if (counter > 0) {
        pf("%s", dirs[0]);
    }
    for (int i = 1; i < counter; i++) {
        pf("  %s", dirs[i]);
    }
    pfc("\n", 0);
}

void touch() {
    int i = 0;
    signed char offset = 0;

    if (token_count < 2) {
        pf("Too few arguments for command touch.");
        return;
    }

    for (i = 1; i < token_count; i++) {
        offset += strlen(tokens[i]);

        int f = creat(tokens[i], 00444);
        if (f == -1) {
            perrorfc("touch", errno);
            return;
        } else lastex = 0;
    }

    if (offset < 0) {
        guard = 1;
    }
}

int main(int argc, char **argv) {
    setup();

	signal(SIGCHLD, process);

    sh_name = (char*) malloc(100);
    user = (char*) malloc(20);
    host = (char*) malloc(20);

	strcpy(sh_name, "agresh - The AlwaysGuilty-Red_Epicness Shell");
    strcpy(user, "competitor");
    strcpy(host, "shellstraction");

    if (getcwd(path, sizeof(path)) == NULL) {
        perrorfc("getcwd", errno);
        exit(lastex);
    }

    size_t size = 500;
    char* line = (char*) malloc(size);
    memset(line, 0, 500);

	while (1) {
        pf("%s@%s:%s$ ", user, host, path);

	    int out = getline(&line, &size, stdin);
        if (out == -1) {
            break;
	    }
	    tokenize(line);
	    if (token_count == 0) {
	        continue;
	    }


	    if (strcmp(tokens[token_count - 1], "&") == 0) {
	        background = 1;
	        token_count--;
	    } else {
	        background = 0;
	    }


	    int cpid1 = -1;
	    if (background == 1) {
	        cpid1 = fork();
	        if (cpid1 != 0) continue;
	    }
	    if (strcmp(tokens[0], "name") == 0)             name();
	    else if (strcmp(tokens[0], "help") == 0)        help();
        else if (strcmp(tokens[0], "whoami") == 0)      whoami();
        else if (strcmp(tokens[0], "hostname") == 0)    hostname();
	    else if (strcmp(tokens[0], "status") == 0)      status();
	    else if (strcmp(tokens[0], "exit") == 0)        exit_shell();
	    else if (strcmp(tokens[0], "print") == 0)       print();
	    else if (strcmp(tokens[0], "echo") == 0)        echo();
	    else if (strcmp(tokens[0], "cd") == 0)          dirchange();
	    else if (strcmp(tokens[0], "pwd") == 0)         dirwhere();
	    else if (strcmp(tokens[0], "mkdir") == 0)       dirmake();
	    else if (strcmp(tokens[0], "ls") == 0)          dirlist();
        else if (strcmp(tokens[0], "touch") == 0)       touch();
        else if (strcmp(tokens[0], "note") == 0)        eton();
	    else pf("Unknown command.");
        
	    if (cpid1 == 0) {
	        break;
	    }

        memset(line, 0, 500);

	}

    freenull(line);
    freenull(sh_name);
    freenull(user);
    freenull(host);

    return lastex;
}
