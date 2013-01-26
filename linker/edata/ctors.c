#include <stdio.h>

int count = 0;

void init1()
{
    count++;
    printf("ctors test. (init1)\n");
}

void init2()
{
    count++;
    count++;
    printf("ctors test. (inti2)\n");
}

void (*fp1)(void) __attribute__((section(".ctors"))) = init1;
void (*fp2)(void) __attribute__((section(".ctors"))) = init2;

int main()
{
    printf("%d\n", count);
    return 0;
}
