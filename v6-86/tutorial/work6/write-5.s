! write(1, hello, 6);
mov ax, #1
int 7
.data1 4
.data2 hello, 6

! bx = hello
! ax = 0x4548
! *(uint8_t *)bx = ah;
! *(uint8_t *)(bx + 1) = al;
mov bx, #hello
mov ax, #0x4548
movb (bx), al
movb 1(bx), ah

! write(1, hello, 6);
mov ax, #1
int 7
.data1 4
.data2 hello, 6

! bx = hello;
! ch = 'H';
! cl = 'E';
! *(uint16_t *)bx = cx;
mov bx, #hello
movb ch, #'H'
movb cl, #'E'
mov (bx), cx

! write(1, hello, 6);
mov ax, #1
int 7
.data1 4
.data2 hello, 6

! exit(0)
mov ax, #0
int 7
.data1 1

.sect .data
hello: .ascii "hello\n"
