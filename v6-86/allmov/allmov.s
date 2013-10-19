mov ax, #1
mov cx, #3
mov dx, #280
mov sp, #5
mov (si), #11
mov (di), #12
mov (bx), #2
mov 2(bx), #2
mov -2(bx), #2
mov 280(bx), #2
mov (bp), #10
mov 2(bp), #10
mov 0x100, #10

mov ax, #0
int 7
.data1 1

.sect .data
hello: .ascii "hello\n"
