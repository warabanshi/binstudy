BITS 64
GLOBAL _start

SECTION .bss
    mem     resb    30000

SECTION .text
_start:
#    lea     rbx, mem
#    ret
