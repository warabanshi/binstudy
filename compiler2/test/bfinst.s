.intel_syntax noprefix
.comm mem, 30000
.globl main

main:
    lea     rbx, mem

    inc     rbx     # >
    dec     rbx     # <

    inc     byte ptr [rbx]  # +
    dec     byte ptr [rbx]  # -

    # .
    mov     rdi, [rbx]
    call    putchar

    # ,
    call    getchar
    mov     [rbx], rax
    
    # exit(0);
    mov     edi, 0
    call    exit
