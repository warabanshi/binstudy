.intel_syntax noprefix
.comm mem, 30000
.globl main

main:
    lea     rbx, mem

    # read systemcall
    mov     rax, 0
    mov     edx, 0x1            # 3nd argument (count)
    mov     rsi, rbx            # 2nd argument (string pointer)
    mov     edi, 0x0            # 1st argument (stdout)
    syscall

#   # write systemcall
#   #mov     byte ptr [rbp], 0x41
#   mov     rax, 1              # system call number
#   mov     edx, 0x1            # 3nd argument (count)
#   mov     rsi, rbp            # 2nd argument (string pointer)
#   mov     edi, 0x1            # 1st argument (stdout)
#   syscall 
