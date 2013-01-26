#include <stdio.h>

extern int a;

int main() {
    a = 2;
    printf("%d\n", a);

    return 0;
}
