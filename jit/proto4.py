'''
JIT sample

CFUCNTYEPE() makes function prototype.
how to make a function using by CFUNCTYPE is at first call CFUNCTION() with 
some parameter returns function prototype.
second, call the returned prototype in first step has function address in parameter.
it will return the callable function.

ex. make function "long func(int a, double b)"
CPROTO = CFUNCTION(c_long, c_int, c_double)
func = CPROTO(<function address>)

memmove(a, b, c)
copy from address of b to address of a length c

if you want to get the assemble statement for sample.
how to do it in simple is
1. make a assemble code (ex. sample.s)
2. assemble by as command ($ as sample.s)
3. objdump the result of step 2 ($ objdump -d -M interl a.out)
'''

import sys, struct
from ctypes import *

libc = cdll.LoadLibrary("libc.so.6")
free = libc.free
printf = libc.printf
putchar = libc.putchar

mmap = libc.mmap
mmap.restype = c_void_p
munmap = libc.munmap
munmap.argtype = [c_void_p, c_size_t]

PROT_READ       = 1
PROT_WRITE      = 2
PROT_EXEC       = 4
MAP_PRIVATE     = 2
MAP_ANONYMOUS   = 0x20

def conv64(dw):
    return map(ord, struct.pack("<q" if dw < 0 else "<Q", dw))

codes = (c_ubyte * 128) (
    0x41, 0x54,                                 # push  r12
    0x41, 0x55,                                 # push  r13
    0x53,                                       # push  rbx
    0x49, 0xbd, 0x00, 0x00, 0x00, 0x00, 0x00,   # mov   r13, (long)
    0x00, 0x00, 0x00,
    0x49, 0xc7, 0xc4, 0x1a, 0x00, 0x00, 0x00,   # mov   r12, 0x1a
    0x48, 0xc7, 0xc3, 0x41, 0x00, 0x00, 0x00,   # mov   rbx, 0x41
    0x49, 0x83, 0xfc, 0x00,                     # cmp   r12, 0
# 0x74, 0x0e
# -> 0x0e is the difference from address start of the instruction below
# the (je <end>), (mov rdi,rbx) statement, of is 0x48 to jumping target
# address, (mov rdi, 0xa) statement, of is 0x48.
# it is 14(= 0x0e).
    0x74, 0x0e,                                 # je    <end>
    0x48, 0x89, 0xdf,                           # mov   rdi, rbx
    0x41, 0xff, 0xd5,                           # call  r13
    0x48, 0xff, 0xc3,                           # inc   rbx
    0x49, 0xff, 0xcc,                           # dec   r12
    0xeb, 0xec,                                 # jmp   <loop>
    0x48, 0xc7, 0xc7, 0x0a, 0x00, 0x00, 0x00,   # mov   rdi, 0xa
    0x41, 0xff, 0xd5,                           # call  r13
    0x5b,                                       # pop   rbx
    0x41, 0x5d,                                 # pop   r13
    0x41, 0x5c,                                 # pop   r12
    0xc3,                                       # ret
)

""" invalid code
rax is not preserved register so 'call rax' destruct the value into it.
(-> see also IALPL chapter.9)
r12 have to push to the stack on start of function and pop from stack
on end of function. because if you didn't it, it might bring on the crash
after the end of this code. it means partial of code of python will crash.

codes = (c_ubyte * 64) (
    0x48, 0xb8, 0x00, 0x00, 0x00, 0x00, 0x00,   # mov   rax, (long)
    0x00, 0x00, 0x00,
    0x49, 0xc7, 0xc4, 0x1a, 0x00, 0x00, 0x00,   # mov   r12, 0x1a
    0x48, 0xc7, 0xc3, 0x41, 0x00, 0x00, 0x00,   # mov   rbx, 0x41
    0x49, 0x83, 0xfc, 0x00,                     # cmp   r12, 0
    0x74, 0x10,                                 # je    end
    0x48, 0x89, 0xdf,                           # mov   rdi, rbx
    0xff, 0xd0,                                 # call  rax
    0x48, 0xff, 0xc3,                           # inc   rbx
    0x49, 0xff, 0xcc,                           # dec   r12
    0xeb, 0xea,                                 # jmp   loop
    0x48, 0xc7, 0xc7, 0x0a, 0x00, 0x00, 0x00,   # mov   rdi, 0xa
    0xff, 0xd0,                                 # call  rax
    0xc3,
)
"""

buflen = len(codes)
p = mmap(
    0, buflen,
    PROT_READ | PROT_WRITE | PROT_EXEC,
    MAP_PRIVATE | MAP_ANONYMOUS,
    -1, 0
)

print("buflen = %d, p = %s, address = %s" % (buflen, p, addressof(codes)))

getaddr = CFUNCTYPE(c_void_p, c_void_p)(lambda p: p)
f       = CFUNCTYPE(c_void_p)(p)

print("putchar address = %s" % hex(addressof(putchar)))
print("putchar address = %s" % hex(addressof(libc.putchar)))
libc.printf("putchar address = %p\n", putchar)
print("putchar address = %s" % hex(getaddr(putchar)))

# this is invalid code cause getaddr doesn't get the address of putchar function.
# that gets the implement of putchar
#memmove(p+0x18, getaddr(putchar), 8)
#memmove(p+0x30, getaddr(putchar), 8)

codes[7:15] = conv64(getaddr(putchar))

# for debug
#print map(hex, codes)

memmove(p, addressof(codes), buflen)

#f() 

munmap(p, buflen)
