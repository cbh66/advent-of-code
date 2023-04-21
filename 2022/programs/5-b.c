#include <stdio.h>

const int NUM_STACKS = 9;
const int MAX_STACK_SIZE = 100;

typedef struct Stack {
    unsigned int size;
    char contents[MAX_STACK_SIZE];
} Stack;

void push(char value, Stack *stack) {
    stack->contents[stack->size++] = value;
}

char pop(Stack *stack) {
    return stack->contents[--(stack->size)];
}

int main() {
    Stack stacks[NUM_STACKS];
    stacks[0] = (Stack) { .size = 8, .contents = {'C', 'Z', 'N', 'B', 'M', 'W', 'Q', 'V'} };
    stacks[1] = (Stack) { .size = 6, .contents = {'H', 'Z', 'R', 'W', 'C', 'B'} };
    stacks[2] = (Stack) { .size = 4, .contents = {'F', 'Q', 'R', 'J'} };
    stacks[3] = (Stack) { .size = 8, .contents = {'Z', 'S', 'W', 'H', 'F', 'N', 'M', 'T'} };
    stacks[4] = (Stack) { .size = 7, .contents = {'G', 'F', 'W', 'L', 'N', 'Q', 'P'} };
    stacks[5] = (Stack) { .size = 3, .contents = {'L', 'P', 'W'} };
    stacks[6] = (Stack) { .size = 8, .contents = {'V', 'B', 'D', 'R', 'G', 'C', 'Q', 'J'} };
    stacks[7] = (Stack) { .size = 5, .contents = {'Z', 'Q', 'N', 'B', 'W'} };
    stacks[8] = (Stack) { .size = 7, .contents = {'H', 'L', 'F', 'C', 'G', 'T', 'J'} };

    int count, source, destination;
    Stack temp = { .size = 0 };
    int i = 0;
    while (scanf("move %i from %i to %i\n", &count, &source, &destination) != EOF) {
        for (int i = 0; i < count; ++i) {
            push(pop(&stacks[source - 1]), &temp);
        }
        for (int i = 0; i < count; ++i) {
            push(pop(&temp), &stacks[destination - 1]);
        }
    }
    for (int i = 0; i < NUM_STACKS; ++i) {
        printf("%c", pop(&stacks[i]));
    }
    return 0;
}
