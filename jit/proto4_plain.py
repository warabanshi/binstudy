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

buflen = len(codes)
p = mmap(
    0, buflen,
    PROT_READ | PROT_WRITE | PROT_EXEC,
    MAP_PRIVATE | MAP_ANONYMOUS,
    -1, 0
)

getaddr = CFUNCTYPE(c_void_p, c_void_p)(lambda p: p)
f       = CFUNCTYPE(c_void_p)(p)

codes[7:15] = conv64(getaddr(putchar))
memmove(p, addressof(codes), buflen)

f() 

munmap(p, buflen)
