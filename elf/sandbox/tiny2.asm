BITS 64
EXTERN _exit
GLOBAL _start
SECTION .text
_start:
    mov     edi, 42
    call    _exit
