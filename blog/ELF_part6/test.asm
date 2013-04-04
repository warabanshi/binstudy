BITS 64
EXTERN putchar
EXTERN exit
GLOBAL _start

SECTION .text
_start:
    mov     edi, 'T'
    call    putchar
    mov     edi, 42
    call    exit
