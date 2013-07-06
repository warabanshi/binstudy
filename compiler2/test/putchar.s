.intel_syntax noprefix
.globl main

main:
    mov     edi, 0x41
    call    putchar
    mov     edi, 0xa
    call    putchar

    mov     edi, 0
    call    exit
