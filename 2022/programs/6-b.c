#include <stdio.h>

const int SIZE = 14;

int distinct(char values[SIZE]) {
    for (int i = 0; i < SIZE; ++i) {
        for (int j = i + 1; j < SIZE; ++j) {
            if (values[i] == values[j]) return 0;
        }
    }
    return 1;
}

int main() {
    char most_recent[SIZE];
    int pos = 0;
    while ((most_recent[pos % SIZE] = getchar()) != EOF) {
        if (pos++ >= SIZE && distinct(most_recent)) break;
    }
    printf("pos: %d\n", pos);
    return 0;
}
