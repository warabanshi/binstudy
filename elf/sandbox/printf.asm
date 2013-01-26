BITS 64
EXTERN printf
EXTERN exit
GLOBAL _start

SECTION .data
output: db  'output char'

SECTION .text
_start:
    mov     edi, output
    call    printf
    mov     edi, 42
    call    exit
