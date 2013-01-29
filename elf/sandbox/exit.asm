BITS 64
EXTERN exit
GLOBAL _start

SECTION .text
_start:
    mov     edi, 42
    call    exit
