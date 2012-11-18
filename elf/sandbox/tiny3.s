BITS 64
GLOBAL _start
SECTION .text
_start:
    mov     eax,    60
    mov     edi,    42
    syscall
