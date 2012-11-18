BITS 64
EXTERN _exit
GLOBAL _start
SECTION .text
_start:
#    push    42     ; ELF64 can't use the push for pass the arguments.
#                   ; you must use mov instruction to specific register.
    mov     edi, 42
    call    _exit
