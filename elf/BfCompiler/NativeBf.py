import sys, struct
from ctypes import *

class NativeBf:

    nativeCodeList  = []

    def __init__(self, src):
        self.nativeCodeList = self.makeNativeCodeList(src)

    def conv32(self, dw):
        return map(ord, struct.pack( "<l" if dw < 0 else "<L", dw))

    def conv64(self, qw):
        return map(ord, struct.pack("<q" if qw < 0 else "<Q", qw))

    def getNativeCodeList(self):
        return self.nativeCodeList

    def makeNativeCodeList(self, src):

        r           = []    #result
        spos        = 0
        loop_index_stack    = []

        # initialize
        ## push r12
        r.extend([0x41, 0x54])
        ## push r13
        r.extend([0x41, 0x55])
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
            s = src[spos]

            if spos >= len(src) - 1:
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
                r.extend([0x48, 0x8b, 0x3b])
                # call  r12
                r.extend([0x41, 0xff, 0xd4])

            elif s == ',':
                # call  getchar
                r.extend([0x41, 0xff, 0xd5])
                # mov   [rbx], rax
                r.extend([0x48, 0x89, 0x03])

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
                r[len(r)-4:len(r)] = self.conv32(back_diff)

                forward_diff = len(r) - (loop_index + 9)
                r[loop_index+5:loop_index+9] = self.conv32(forward_diff)

            spos += 1

        ## pop r13
        r.extend([0x41, 0x5d])
        ## pop r12
        r.extend([0x41, 0x5c])
        ## ret
        r.extend([0xc3])
        return r

    def execute(self, outputTarget = ''):
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

        bf_mem = (c_ubyte * 30000)()
        bf_code = self.nativeCodeList

        mmap.restype = POINTER(ARRAY(c_ubyte, len(bf_code)))
        p = mmap(
            0, len(bf_code),
            PROT_READ | PROT_WRITE | PROT_EXEC,
            MAP_PRIVATE | MAP_ANONYMOUS,
            -1, 0
        )[0]

        getaddr = CFUNCTYPE(c_void_p, c_void_p)(lambda p: p)
        f       = CFUNCTYPE(c_void_p)(getaddr(p))

        bf_code[6:14]   = self.conv64(getaddr(bf_mem))
        bf_code[16:24]  = self.conv64(getaddr(putchar))
        bf_code[26:34]  = self.conv64(getaddr(getchar))

        p[:] = bf_code
        f()

        if (len(outputTarget) > 0):
            #print map(hex, bf_code)
            with open(outputTarget, "wb") as fp:
                fp.write(p)

        munmap(p, len(bf_code))


