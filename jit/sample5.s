.intel_syntax noprefix
.comm mem, 30000
.globl main

main:
    mov     rbx, 0x123456789abcdef0
    push    r12
    push    r13
    mov     r12, 0x123456789abcdef0
    mov     r13, 0x123456789abcdef0
    inc     rbx
    dec     rbx
    inc     byte ptr [rbx]
    dec     byte ptr [rbx]
    mov     rdi, [rbx]
    call    r12

    call    r13
    mov     [rbx], rax

start_loop_0:
    cmp     byte ptr [rbx], 0
    jz      end_loop_0
    
    jmp     start_loop_0
end_loop_0:
    pop     r13
    pop     r12
    ret
