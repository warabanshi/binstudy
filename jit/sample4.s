.intel_syntax noprefix
.globl main

main:
    mov     r12, 26
    mov     rbx, 0x41

loop:
    cmp     r12, 0
    jz      end

    mov     rdi, rbx
    call    putchar

    inc     rbx
    dec     r12
    jmp     loop

end:
    mov     rdi, 0xa
    call    putchar
