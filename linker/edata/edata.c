/**
 * linker script referenced by /usr/lib64/ldscripts/elf_x86_64.x
 */
#include <stdio.h>

extern int __fini_array_end;
extern int edata;
extern int end;

int main()
{
    printf("&__fini_array_end = 0x%016lx\n", (long) &__fini_array_end);
    printf("&edata            = 0x%016lx\n", (long) &edata);
    printf("&end              = 0x%016lx\n", (long) &end);

    return 0;
}
