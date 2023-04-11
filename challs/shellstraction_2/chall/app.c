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


// macros
// #define ee(code, errstr);               fprintf(stderr, "%s: %d\n", errstr, code); fflush(NULL); exit(1);
// #define pf(str)                      fprintf(stdout, str); fflush(NULL);
#define pf(format, ...);                fprintf(stdout, (format), ##__VA_ARGS__); fflush(NULL);
#define pfc(format, retval, ...);       fprintf(stdout, (format), ##__VA_ARGS__); fflush(NULL); lastex = retval;
#define perrorfc(str, errcode);         perror(str); lastex = errcode;
#define pc(format, retval, ...);        fprintf(stdout, (format), ##__VA_ARGS__); lastex = retval;
#define fc(retval);                     fflush(NULL); lastex = retval;
#define freenull(ptr);                  free(ptr); ptr = NULL;



// AG
char* user;
char* host;
char path[200];

int guard = 0;

char* notes_arr[10];

// RE
int token_count;
char* tokens[50];           // token pointers array limited to 50 pointers??
char* sh_name;
int statp;
int background = 0;
/* int file_in = 0;
char* file_in_name;
int file_out = 0;
char* file_out_name; */
int lastex = 0;

// sighandler
void process(int s) {
    switch (s) {
        case 17: // SIGCHLD
            wait(&statp);
            return;
    }
}

// IO setup
void setup() {
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);
    setvbuf(stderr, 0, _IONBF, 0);
}

// stores pointers to the first characters of tokens/multitokens (tokens wrapped in quotation marks) in the global tokens array
// this function does not check for tokens array bounderies
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
        //printf(":%c: %d %d %d\n", curr, token_count, newtoken, multitoken);
        if (newtoken == 1) {
            // check for max token count
            if (token_count > 50) {
                puts("Too many tokens.");
                fflush(stdout);
                return;
            }

            if (isspace(curr) != 0) {        // isspace checks for white-space character, returns nonzero if curr is a white-space
                line[i] = '\0';
                continue;
            }
            if (curr == '"') {
                multitoken = 1;
                tokens[token_count] = &(line[i+1]);
            }
            else {
                multitoken = 0;
                tokens[token_count] = &(line[i]);       // it stores address of the first char of the token in the tokens array
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

// my favourite function, thanks Mitič, very cool
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

    // formats
    // note add 0 asokidfh
    // note remove 0
    // note show 0 

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
            strncpy(notes_arr[index], tokens[4], strlen(tokens[4]));        // this copies input token on heap, without the nullbyte
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
        // atoi doesnt detect errors, strtol can do the same thing plus error detection
        exit_code = (int) strtol(tokens[1], NULL, 10);
        // exit(atoi(tokens[1]));
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
    // zakaj printamo posebej prvi token in potem vse ostale?
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

// cd
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

// pwd
void dirwhere() {
    if (getcwd(path, sizeof(path)) != NULL) {
        pfc("%s\n", 0, path);
    } else {
        perrorfc("pwd", errno);
    }
}

// mkdir
void dirmake() {
    int out = mkdir(tokens[1], 0755);
    if (out != 0) {
        perrorfc("mkdir", errno);
    }
    else lastex = 0;
}

// ls
// prints dir entries, not sorted
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
        //printf("%s ", nm);
        //if (strcmp(".", nm) == 0 || strcmp("..", nm) == 0) continue;
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

// creates a file with a given path and only with read perms for everybody
void touch() {
    int i = 0;
    signed char offset = 0;

    if (token_count < 2) {
        pf("Too few arguments for command touch.");
        return;
    }

    for (i = 1; i < token_count; i++) {
        // copy dir's name from tokens array onto the stack
        // there is 50 tokens max
        offset += strlen(tokens[i]);

        // create a dir with a given name
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

/// @brief 
/// @param argc 
/// @param argv 
/// @return 
int main(int argc, char **argv) {
    setup();

	signal(SIGCHLD, process);

    sh_name = (char*) malloc(100);
    user = (char*) malloc(20);
    host = (char*) malloc(20);

    // TODO: replace with strncpy
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
        // i had to comment this part out, otherwise the server wouldn't print the prompt when connected to via nc 
	    /* if (isatty(1)) {
            printf("%s@%s:%s$ ", user, host, path);
        } */
        pf("%s@%s:%s$ ", user, host, path);

	    int out = getline(&line, &size, stdin);         // stores pointer to buffer to *lineptr and updates *n with buffer size, returns number of chars read
        if (out == -1) {                                // failure or EOF
            break;
	    }
	    tokenize(line);
	    if (token_count == 0) {
	        continue;
	    }


        // should we run this program in the background?
	    if (strcmp(tokens[token_count - 1], "&") == 0) {
	        background = 1;
	        token_count--;
	    } else {
	        background = 0;
	    }

        // order of file redirection: <inFile, >outFile, &

        // redirect output into another file?                       // i commented these out because competetitors could've overwritten flag.txt file with "echo adsjhf >flag.txt"
	    /* if (tokens[token_count - 1][0] == '>') {
	        file_out = 1;
	        file_out_name = &(tokens[token_count-1][1]);
	        token_count--;
	    } else {
	        file_out = 0;
	    } */

        // redirect input from another file?
	    /* if (tokens[token_count - 1][0] == '<') {
	        file_in = 1;
	        file_in_name = &(tokens[token_count-1][1]);
	        token_count--;
	    } else {
	        file_in = 0;
	    } */

	    /* printf("\nTokens:\n");
	    for (int i = 0; i < token_count; i++) {
	        printf(":%s:\n", tokens[i]);
	    }
	    printf("Modifiers: IN_REDIR=%d (%s) OUT_REDIR=%d (%s) BKGRND=%d\n\n", file_in, file_in_name, file_out, file_out_name, background); */

        // creating background process
	    int cpid1 = -1;
	    if (background == 1) {
	        cpid1 = fork();
	        if (cpid1 != 0) continue;       // if not in child, continue
	    }

        // open files for redirecting input/output
	    /* FILE* old_stdout = stdout;
	    if (file_out == 1) {
	        stdout = fopen(file_out_name, "w");
            if (stdout == NULL) {
                stdout = old_stdout;
                perror("Output redirection");
                fflush(stdout);
                continue;               // are errors here handled correctly? i don't know.
            }
	    }

	    FILE* old_stdin = stdin;
	    if (file_in == 1) {
	        stdin = fopen(file_in_name, "r");
            if (stdin == NULL) {
                stdin = old_stdin;
                perror("Input redirection");
                fflush(stdout);
                continue;
            }
	    } */


        // make it so that it saves the user's random dir names on heap?

        // evaluating the tokens
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
        
        // are we in the child process?
	    if (cpid1 == 0) {
	        break;
	    }
        // handlers for inpt/output redirection finalization
	    /* if (file_out == 1) {
	        stdout = old_stdout;
	    }
	    if (file_in == 1) {
	        stdin = old_stdin;
	    } */

        memset(line, 0, 500);

	}

    freenull(line);
    freenull(sh_name);
    freenull(user);
    freenull(host);

    return lastex;
}
