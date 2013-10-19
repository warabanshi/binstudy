! mov immediate to register/memory
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

! mov register/memory to/from register
mov ax, bp
mov ax, 2(bp)
mov cx, bp
mov cx, 0x100

! mov memory to accumulator
mov ax, 0xf
mov ax, 0x100

! mov accumulator to memory
mov 0xf, ax
mov 0x100, ax

! mov register/memory to SegmentRegister

! mov SegmentRegister to register/memory

mov ax, #0
int 7
.data1 1

.sect .data
hello: .ascii "hello\n"
