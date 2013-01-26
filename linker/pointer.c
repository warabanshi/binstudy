#include <stdio.h>

char s1[] = "This is array.";
char *s2  = "This is pointer.";

int main() {
    printf("  s1 = 0x%016lx\n", (unsigned long)s1);
    printf(" &s1 = 0x%016lx\n", (unsigned long)&s1);
    printf("  s2 = 0x%016lx\n", (unsigned long)s2);
    printf(" &s2 = 0x%016lx\n", (unsigned long)&s2);
    printf("sizeof(s1) = %ld\n", sizeof(s1));
    printf("sizeof(s2) = %ld\n", sizeof(s2));

    return 0;;
}
