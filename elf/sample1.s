.intel_syntax noprefix
.globl main

#    .section    .rodata
#.LC0:
#    .string     "Hello "
#.LC1:
#    .string     "World!"

main:
    mov     rax, 0x41
    add     rax, 0x10
