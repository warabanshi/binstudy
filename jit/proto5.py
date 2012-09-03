'''
JIT sample 2

---- memo ----
how to get the memory space in simply way for brainf*ck is
grub the memory space by python instruction and pass the address of it.

'''

import sys, struct
from ctypes import *

libc = cdll.LoadLibrary("libc.so.6")
free = libc.free
printf = libc.printf
putchar = libc.putchar
getchar = libc.getchar

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

def translate(source, r):
    spos        = 0
    loop_label  = 0
    loop_stack  = []

    # initialize
    ## push r12
    ## push r13
    ## mov  rbx, 0x0000000000000000  (for set buffer)
    r.extend([0x48, 0xbb])
    r.extend([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    ## mov  r12, 0x0000000000000000  (for set putchar)
    r.extend([0x49, 0xbc])
    r.extend([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    ## mov  r13, 0x0000000000000000  (for set getchar)
    r.extend([0x49, 0xbd])
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
            # mov   rdi, [rbx]
            # call  putchar
            r.extend([0x48, 0x8b, 0x3b, 0x41, 0xff, 0xd4])

        elif s == ',':
            # call  getchar
            # mov   [rbx], rax
            r.extend([0x41, 0xff, 0xd5, 0x48, 0x89, 0x03])

        elif s == '[':
            # start_(loop_name):
            # cmp   byte ptr [rbx], 0
            # jz    end_(loop_name)
            None

        elif s == ']':
            # jmp   start_(loop_name)
            # end_(loop_name):
            None

        spos += 1

    ## pop r13
    ## pop r12
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

print "bf_mem = %s, putchar = %s, getchar = %s" % (hex(getaddr(bf_mem)), hex(getaddr(putchar)), hex(getaddr(getchar)))

bf_code[2:10]    = conv64(getaddr(bf_mem))
bf_code[12:20]  = conv64(getaddr(putchar))
bf_code[22:30]  = conv64(getaddr(getchar))

# for debug
print map(hex, bf_code)

#memmove(p, addressof(bf_code), len(bf_code))
print len(p), len(bf_code)
p[:] = bf_code
f()

munmap(p, len(bf_code))

''' proto5.py
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

# for debug
#print map(hex, codes)

memmove(p, addressof(codes), buflen)

f() 

munmap(p, buflen)
'''
