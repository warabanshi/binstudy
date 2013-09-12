! write(1, hello, 6);
mov ax, #1
int 7
.data1 4
.data2 hello, 6

! bx = hello;
! ax = 0x4548;
! *(uint16_t *)bx = ax;
mov bx, #hello
mov ax, #0x4548
mov (bx), ax

! write(1, hello, 6);
mov ax, #1
int 7
.data1 4
.data2 hello, 6

! bx = hello;
! cx = 0x4c4c;
! *(uint16_t *)(bx + 2) = cx;
mov bx, #hello
mov cx, #0x4c4c
mov 2(bx), cx

! write(1, hello, 6);
mov ax, #1
int 7
.data1 4
.data2 hello, 6

! exit(0);
mov ax, #0
int 7
.data1 1

.sect .data
hello: .ascii "hello\n"
