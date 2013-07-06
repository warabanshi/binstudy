.intel_syntax noprefix
.comm mem, 30000
.globl main

main:
    #mem[0] = 65;
    mov byte ptr mem, 65

    # putchar(mem[0]);
    movzx edi, byte ptr mem
    call putchar
        
    # mem[0]++;
    inc byte ptr mem

    # putchar(mem[0]);
    movzx edi, byte ptr mem
    call putchar

    # exit(0);
    mov edi, 0
    call exit
