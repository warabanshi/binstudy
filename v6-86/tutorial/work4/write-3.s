! write(1, hello, 6);
mov ax, #1
int 7 
.data1 4
.data2 hello, 6

! bx = hello;
! *(uint8_t *)bx = 'H';
mov bx, #hello
movb (bx), #'H'

! write(1, hello, 6);
mov ax, #1
int 7
.data1 4
.data2 hello, 6

! bx = hello;
! *(uint8_t *)(bx + 2) = 'L'
mov bx, #hello
movb 2(bx), #'L'

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
