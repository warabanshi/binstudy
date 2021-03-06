'''
JIT sample 3

---- memo ----
if you call a system call instead of libc functions for putchar and etc,
then you have no need to implant the address of its address.

this version use system call
'''

import sys, struct
from ctypes import *

libc = cdll.LoadLibrary("libc.so.6")
free = libc.free

mmap = libc.mmap
mmap.restype = c_void_p
munmap = libc.munmap
munmap.argtype = [c_void_p, c_size_t]

PROT_READ       = 1
PROT_WRITE      = 2
PROT_EXEC       = 4
MAP_PRIVATE     = 2
MAP_ANONYMOUS   = 0x20

def conv16(w):
    return map(ord, struct.pack("<h" if w < 0 else "<H", w))

def conv32(dw):
    return map(ord, struct.pack("<l" if dw < 0 else "<L", dw))

def conv64(qw):
    return map(ord, struct.pack("<q" if qw < 0 else "<Q", qw))

def translate(source, r):
    spos        = 0

    loop_index_stack    = []
    jmp_index_stack   = []
    back_index_stack  = []

    # initialize
    ## push rbx
    r.extend([0x53])
    ## mov  rbx, 0x0000000000000000  (for set buffer)
    r.extend([0x48, 0xbb])
    r.extend([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    while True:
        s = source[spos]

        if spos >= len(source) - 1:
            break

        elif s == '>':
            # inc   rbx
            r.extend([0x48, 0xff, 0xc3])

        elif s == '<':
            # dec   rbx
            r.extend([0x48, 0xff, 0xcb])

        elif s == '+':
            # inc   byte ptr [rbx]
            r.extend([0xfe, 0x03])

        elif s == '-':
            # dec   byte ptr [rbx]
            r.extend([0xfe, 0x0b])

        elif s == '.':
            # mov   rax, 1      (set system call to write)
            r.extend([0x48, 0xc7, 0xc0, 0x01, 0x00, 0x00, 0x00])
            # mov   edx, 0x1    (3rd argument)
            r.extend([0xba, 0x01, 0x00, 0x00, 0x00])
            # mov   rsi, rbx    (2rd argument)
            r.extend([0x48, 0x89, 0xde])
            # mov   edi, 0x1    (1rd argument)
            r.extend([0xbf, 0x01, 0x00, 0x00, 0x00])
            # syscall
            r.extend([0x0f, 0x05])

        elif s == ',':
            # mov   rax, 0      (set sysytem call to read)
            r.extend([0x48, 0xc7, 0xc0, 0x00, 0x00, 0x00, 0x00])
            # mov   edx, 0x1
            r.extend([0xba, 0x01, 0x00, 0x00, 0x00])
            # mov   rsi, rbx
            r.extend([0x48, 0x89, 0xde])
            # mov   edi, 0x0
            r.extend([0xbf, 0x00, 0x00, 0x00])
            # syscall
            r.extend([0x0f, 0x05])

        elif s == '[':
            # start_(loop_name):
            # cmp   byte ptr [rbx], 0
            # jz    dword end_(loop_name)
            loop_index_stack.append(len(r))
            r.extend([0x80, 0x3b, 0x00])
            r.extend([0x0f, 0x84, 0x00, 0x00, 0x00, 0x00])

        elif s == ']':
            # jmp   dword start_(loop_name)
            # end_(loop_name):
            r.extend([0xe9, 0x00, 0x00, 0x00, 0x00])
            loop_index = loop_index_stack.pop()

            back_diff = loop_index - len(r)
            r[len(r)-4:len(r)] = conv32(back_diff)

            forward_diff = len(r) - (loop_index + 9)
            r[loop_index+5:loop_index+9] = conv32(forward_diff)

        spos += 1

    ## pop rbx
    r.extend([0x5b])
    ## ret
    r.extend([0xc3])
    return r

"""
bf_mem = mmap(
    0, 30000,
    PROT_READ | PROT_WRITE | PROT_EXEC,
    MAP_PRIVATE | MAP_ANONYMOUS,
    -1, 0
)
"""
bf_mem = (c_ubyte * 30000)()

f = open(sys.argv[1])
source = f.read()
f.close()

bf_code = []
bf_code = translate(source, bf_code)

mmap.restype = POINTER(ARRAY(c_ubyte, len(bf_code)))
p = mmap(
    0, len(bf_code),
    PROT_READ | PROT_WRITE | PROT_EXEC,
    MAP_PRIVATE | MAP_ANONYMOUS,
    -1, 0
)[0]

getaddr = CFUNCTYPE(c_void_p, c_void_p)(lambda p: p)
f       = CFUNCTYPE(c_void_p)(getaddr(p))

bf_code[3:11]   = conv64(getaddr(bf_mem))

# for debug
#print map(hex, bf_code)

#memmove(p, addressof(bf_code), len(bf_code))
p[:] = bf_code
with open('jit.out', "wb") as fp:
    fp.write(p)
f()

munmap(p, len(bf_code))

