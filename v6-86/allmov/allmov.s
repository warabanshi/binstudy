mov ax, #1
mov bx, #2
mov cx, #3
mov dx, #4
mov sp, #5
mov bp, #10
mov si, #11
mov di, #12

mov ax, #1
int 7
.data1 4

.sect .data
hello: .ascii "hello\n"
