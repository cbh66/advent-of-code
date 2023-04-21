#include <stdio.h>

int main() {
    int a, b, c, d;
    int sum = 0;
    while (scanf("%d-%d,%d-%d", &a, &b, &c, &d) != EOF) {
        int disjoint = ((b < c) || (d < a));
        sum += !disjoint;
    }
    printf("sum: %d\n", sum);
    return 0;
}
