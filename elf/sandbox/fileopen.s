.intel_syntax noprefix
.comm mem, 30000
#.comm filepath, 128
.globl main

#.data
#format: .asciz  "%s\n"

main:
    #lea     rbx, mem

    # get argv[0]
    #push    rbp
    #sub     rsp, 8
    #mov     rax, 0
    #mov     rdi, format
    #mov     rsi, [rsp+32]
    #call    printf

  
    pop     ecx             # return address
    pop     ecx             # argc
    pop     ecx             # argv
    mov     ecx, [ecx+4]    # 


#    # open systemcall
#    mov     rax, 2
#    mov     rsi, rbx
#    mov     rdi, filepath
#    syscall

#    # read systemcall
#    mov     rax, 0
#    mov     edx, 0x1            # 3nd argument (count)
#    mov     rsi, rbx            # 2nd argument (string pointer)
#    mov     edi, 0x0            # 1st argument (stdin)
#    syscall

#   # write systemcall
#   #mov     byte ptr [rbp], 0x41
#   mov     rax, 1              # system call number
#   mov     edx, 0x1            # 3nd argument (count)
#   mov     rsi, rbp            # 2nd argument (string pointer)
#   mov     edi, 0x1            # 1st argument (stdout)
#   syscall 
