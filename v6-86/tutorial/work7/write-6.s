! write(1, hello, 6);
mov ax, #1
int 7
.data1 4
.data2 hello, 6

! *(uint16_t *)hello = 0x4548;
mov hello, #0x4548

! write(1, hello, 6);
mov ax, #1
int 7
.data1 4
.data2 hello, 6

! *(uint16_t *)(hello + 2) = 0x4c4c
mov hello + 2, #0x4c4c

! write(1, hello, 6);
mov ax, #1
int 7
.data1 4
.data2 hello, 6

! *(uint8_t *)(hello + 4) = 'O';
movb hello + 4, #'O'

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
