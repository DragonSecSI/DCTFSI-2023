#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

#define N 0b1000
#define W 0b0100
#define S 0b0010
#define E 0b0001
#define C 20

int solved;

void disp_maze(int maze[C][C]) {
    printf("        start\n          |\n          V\n");
    for (int i = 0; i < C; i++) {
        for (int j = 0; j < C; j++) {
            printf("%c", maze[i][j]+'@');
        }       
        printf("\n");
    }
    printf("          A\n          |\n        finish\n");
    printf("\n");
}

int visit(int maze[C][C], int d, int curri, int currj) {
    if (d == N&& curri-1>=0) {
        return maze[curri-1][currj];
    } else if (d == W&& currj-1>=0) {
        return maze[curri][currj-1];
    } else if (d == S&& curri+1<C) {
        return maze[curri+1][currj];
    } else if (d == E&& currj+1<C) {
        return maze[curri][currj+1];
    } else return -1;
}

int neigh(int maze[C][C], int curri, int currj) {
    //Return amount of neighbors that have not been yet visited.
    int sum = 0;
    if (curri-1 >= 0 && maze[curri-1][currj] == 0) sum++;
    if (currj-1 >= 0 && maze[curri][currj-1] == 0) sum++;
    if (curri+1 < C && maze[curri+1][currj] == 0) sum++;
    if (currj+1 < C && maze[curri][currj+1] == 0) sum++;
    return sum;
}

void mazegen(int maze[C][C], int curri, int currj, int endi, int endj, char* buf, int ind) {
    if (curri == endi && currj == endj) {
        solved = 1;
    }
    while (neigh(maze,curri,currj) > 0) {
        int direction;
        do {
            direction = 1 << (rand() % 4);
        } while (visit(maze, direction, curri, currj) != 0);
        //found neighbor that can be visited
        if (solved == 0) {
            if (direction == N) buf[ind] = 'N';
            else if (direction == W) buf[ind] = 'W';
            else if (direction == S) buf[ind] = 'S';
            else if (direction == E) buf[ind] = 'E';
            ind++;
        }

        if (direction == N) {
            maze[curri][currj] = maze[curri][currj] | N;
            maze[curri-1][currj] = maze[curri-1][currj] | S;
            mazegen(maze, curri-1, currj, endi, endj, buf, ind);
        } else if (direction == W) {
            maze[curri][currj] = maze[curri][currj] | W;
            maze[curri][currj-1] = maze[curri][currj-1] | E;
            mazegen(maze, curri, currj-1, endi, endj, buf, ind); 
        } else if (direction == S) {
            maze[curri][currj] = maze[curri][currj] | S;
            maze[curri+1][currj] = maze[curri+1][currj] | N;
            mazegen(maze, curri+1, currj, endi, endj, buf, ind);
        } else if (direction == E) {
            maze[curri][currj] = maze[curri][currj] | E;
            maze[curri][currj+1] = maze[curri][currj+1] | W;
            mazegen(maze, curri, currj+1, endi, endj, buf, ind);
        }
        if (solved == 0) {
            buf[ind] = '\0';
            ind--;
        }
    }
}

int main() {
    srand(time(NULL));
    int maze[C][C];
    char* buf = (char*)malloc(C*C*sizeof(char));
    for (int i = 0; i < C; i++) {
        for (int j = 0; j < C; j++) {
            maze[i][j] = 0;
        }       
    }
    
    int starti = 0;
    int startj = 10;
    int endi = 19;
    int endj = 10;
    solved = 0;

    printf("Generating maze...\n");
    mazegen(maze, starti, startj, endi, endj, buf, 0);
    printf("Maze generated!\n");
    printf("If you can get out of this maze in five seconds, I'll give you the flag!\n");
    printf("(Note: you are trying to get from the letter below '|V' to the letter above 'A|'.)\n");
    printf("Ready? Press ENTER to continue!\n");
    while( getchar() != '\n' );
    
    disp_maze(maze);
    int start_time = time(NULL);
    int len = strlen(buf);
    char* input = (char*)malloc(sizeof(char) * (len + 1));
    fgets(input, len+1, stdin);
    int end_time = time(NULL);

    int win = 0;
    for (int i = 0; i <= len; i++) {
        if (buf[i] != input[i]) {
            win = 69;
            break;
        }
    }
    if (end_time - start_time >= 5) {
        printf("Our hero wastes too much time and dies of obsolescence.\n");
    }
    else if (win == 0) {
        system("echo -n \"You have escaped the treacherous maze! The flag is: \"; cat flag.txt");
    } else {
        printf("Our hero is consumed by the bowels of the maze, never to be seen again.\n");
    }


}