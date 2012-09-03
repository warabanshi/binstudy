.intel_syntax noprefix
.globl main

main:
    push    r12
    push    r13
    push    rbx

    mov     r13, 0x123456789abcdef0
    mov     r12, 26
    mov     rbx, 0x41

loop:
    cmp     r12, 0
    jz      end

    mov     rdi, rbx
    call    r13

    inc     rbx
    dec     r12
    jmp     loop

end:
    mov     rdi, 0xa
    call    r13

    pop     rbx
    pop     r13
    pop     r12
    ret
