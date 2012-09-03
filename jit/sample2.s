.intel_syntax noprefix
.globl main

main:
    push    r12
    push    r13
    push    rbx
    mov     r12, 0x12
    mov     rbx, 0x41
    call    r12
    mov     r13, 0x123456789abcdef0
    call    r13
loop:
    cmp     r12, 0
    je      end
    mov     rdi, rbx
    call    r13
    inc     rbx
    dec     r12
    jmp     loop
    pop     r12
    pop     r13
    pop     rbx
end:
    mov     rdi, 0xa
