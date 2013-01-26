#55                      push   rbp
#48 89 e5                mov    rbp,rsp
#48 83 ec 10             sub    rsp,0x10
#//char a = 'A'#
#c6 45 ff 41             mov    BYTE PTR [rbp-0x1],0x41
#//write(1, &a, 1)#
#48 8d 45 ff             lea    rax,[rbp-0x1]
#ba 01 00 00 00          mov    edx,0x1
#48 89 c6                mov    rsi,rax
#bf 01 00 00 00          mov    edi,0x1
#e8 da fe ff ff          call   400420 <write@plt>
#//return #
               
#BITS 64
#GLOBAL main
#SECTION .text
#.comm mem, 30000
#main:
               
#    mov     eax,    1       # number of write systemcall
#    mov     edi,    0x48    # parameter 1
#    mov     
#    syscall

.intel_syntax noprefix
.comm mem, 30000
.globl main

main:
    push    rbx
    lea     rbx, mem
    mov     byte ptr [rbx], 0x41
    mov     rax, 1
    mov     edx, 0x1            # 3nd argument (count)
    mov     rsi, rbx            # 2nd argument (string pointer)
    mov     edi, 0x1            # 1st argument (stdout)
    pop     rbx
    syscall 
