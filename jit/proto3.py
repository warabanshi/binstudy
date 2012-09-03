'''
JIT sample3

implant assembly codes to memory as directly
CFUNCTYPE makes function prototype.
it parameters are first is return value's type
and after are arguments pass to function which will generate from prototype
'''

from ctypes import *

libc = cdll.LoadLibrary("libc.so.6")
free = libc.free
printf = libc.printf

mmap = libc.mmap
mmap.restype = c_void_p
munmap = libc.munmap
munmap.argtype = [c_void_p, c_size_t]

PROT_READ       = 1
PROT_WRITE      = 2
PROT_EXEC       = 4
MAP_PRIVATE     = 2
MAP_ANONYMOUS   = 0x20

codes = (c_ubyte * 32) (
    0x48, 0x89, 0xf8,   # mov rax, rdi
    0x48, 0x01, 0xf0,   # add rax, rsi
    0xc3,               # ret
)

buflen = len(codes)
p = mmap(
    0, buflen,
    PROT_READ | PROT_WRITE | PROT_EXEC,
    MAP_PRIVATE | MAP_ANONYMOUS,
    -1, 0
)

print("buflen = %d, p = %s, address = %s" % (buflen, p, addressof(codes)))

# memmove(dst, src, count)
memmove(p, addressof(codes), buflen)
f = CFUNCTYPE(c_int, c_int, c_int)(p)

print("f(1, 2) = %s" % f(1, 2))
munmap(p, buflen)
