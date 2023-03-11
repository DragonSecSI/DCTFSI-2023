#include <string.h>
#include <stdio.h>

int get_bit(char byte, int position) {
    int mask = 1 << position; //position from 0 to 7.
    int bit = (byte & mask) >> position;
    return bit;
}

int main() {
    FILE* input = fopen("input.txt", "rb");
    FILE* output = fopen("output.txt", "w");
    char c;
    int prev_bit = -1;
    int count = 0;
    while ( (c = fgetc(input)) != EOF) {
        for (int i = 0; i < 8; i++) {
            int curr_bit = get_bit(c, i);
            if (curr_bit == prev_bit) {
                count += 1;
            } else {
                if (prev_bit != -1) {
                    putc('0'+count, output);
                    putc('0'+prev_bit, output);
                }
                prev_bit = curr_bit;
                count = 1;
            }
        }
    }
    fclose(input);
    fclose(output);

}