'''
JIT sample 7

this version make ELF format
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

def makeELF(bf):

    #addr = 0x08048000 if addr == None else addr
    addr = 0x08048000

    # ELF header
    e = []
    e.extend([0x7f, 0x45, 0x4c, 0x46, 0x02, 0x01, 0x01])        # e_ident
    e.extend([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    e.extend([0x02, 0x00])                  # u16 e_type
    e.extend([0x3e, 0x00])                  # u16 e_machine
    e.extend([0x01, 0x00, 0x00, 0x00])      # u32 e_version
    e.extend([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # u64 e_entry
    e.extend([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # u64 e_phoff
    e.extend([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # u64 e_shoff
    e.extend([0x00, 0x00, 0x00, 0x00])      # u32 e_flags
    e.extend([0x00, 0x00])                  # u16 e_ehsize
    e.extend([0x00, 0x00])                  # u16 e_phentisize
    e.extend([0x01, 0x00])                  # u16 e_phnum
    e.extend([0x40, 0x00])                  # u16 e_shentsize
    e.extend([0x03, 0x00])                  # u16 e_shnum
    e.extend([0x01, 0x00])                  # u16 e_shstrndx

    # program header
    p = []
    p.extend([0x01, 0x00, 0x00, 0x00])      # u32 p_type
    p.extend([0x05, 0x00, 0x00, 0x00])      # u32 p_flags
    p.extend([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # u64 p_offset
    p.extend([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # u64 p_vaddr
    p.extend([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # u64 p_paddr
    p.extend([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # u64 p_filesz
    p.extend([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # u64 p_memsz
    p.extend([0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # u64 p_align

    # section string table
    t = []
    t.extend([0x00])                                    # shstrtbl
    t.extend([0x2e, 0x74, 0x65, 0x78, 0x74, 0x00])      # ".text"
    t.extend([0x2e, 0x73, 0x68, 0x73, 0x74, 0x72, 0x74, 0x62, 0x6c, 0x00])
                                                        # ".shstrtbl"

    # section header
    s = []
    # first section header
    s.extend([0x00, 0x00, 0x00, 0x00])
    s.extend([0x00, 0x00, 0x00, 0x00])
    s.extend([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    s.extend([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    s.extend([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    s.extend([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    s.extend([0x00, 0x00, 0x00, 0x00])
    s.extend([0x00, 0x00, 0x00, 0x00])
    s.extend([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    s.extend([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    # second section header
    second_shpos = len(s)
    s.extend([0x00, 0x00, 0x00, 0x00])                          # sh_name
    s.extend([0x03, 0x00, 0x00, 0x00])                          # sh_type
    s.extend([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # sh_flags
    s.extend([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # sh_addr
    s.extend([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # sh_offset
    s.extend([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # sh_size
    s.extend([0x00, 0x00, 0x00, 0x00])                          # sh_link
    s.extend([0x00, 0x00, 0x00, 0x00])                          # sh_info
    s.extend([0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # sh_addralign
    s.extend([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # sh_entsize

    # third section header
    third_shpos = len(s)
    s.extend([0x00, 0x00, 0x00, 0x00])                          # sh_name
    s.extend([0x01, 0x00, 0x00, 0x00])                          # sh_type
    s.extend([0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # sh_flags
    s.extend([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # sh_addr
    s.extend([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # sh_offset
    s.extend([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # sh_size
    s.extend([0x00, 0x00, 0x00, 0x00])                          # sh_link
    s.extend([0x00, 0x00, 0x00, 0x00])                          # sh_info
    s.extend([0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # sh_addralign
    s.extend([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # sh_entsize

    filesize = len(e + p + bf + t + s)

    e[24:32] = conv64(addr + len(e) + len(p))   # set e_entry
    e[32:40] = conv64(len(e))                   # set e_phoff
    e[40:48] = conv64(len(e + p + bf + t))      # set e_shoff
    e[52:54] = conv16(len(e))                   # set e_ehsize
    e[54:56] = conv16(len(p))                   # set e_phentisize

    #p[16:24] = conv64(addr + len(e))                # set p_vaddr
    #p[24:32] = conv64(addr + len(e))                # set p_paddr
    p[16:24] = conv64(addr)                 # set p_vaddr
    p[24:32] = conv64(addr)                 # set p_paddr
    p[32:40] = conv64(filesize)             # set p_filesz
    p[40:48] = conv64(filesize + 30000)     # set p_memsz
    #p[48:56] = conv64(addr + len(e))       # set p_align

    s[64:68] = conv32(7)                # set sh_name
    s[88:96] = conv64(len(e+p+bf))      # set sh_offset
    s[96:104] = conv64(len(t))          # set sh_size

    s[128:132] = conv32(1)              # set sh_name
    s[144:152] = conv64(addr + len(e) + len(p))     # set sh_addr
    s[152:160] = conv64(len(e+p))       # set sh_offset
    s[160:168] = conv64(len(bf))        # set sh_size

    bf[3:11]   = conv64(addr + filesize)

    return e + p + bf + t + s

# dummy
#def translate(source, r):
#    r.extend([0xb8, 0x3c, 0x00, 0x00, 0x00])
#    r.extend([0xbf, 0x2a, 0x00, 0x00, 0x00])
#    r.extend([0x0f, 0x05])
#
#    return r

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
    ## exit
    #r.extend([0xc3])
    return r

#bf_mem = (c_ubyte * 30000)()

f = open(sys.argv[1])
source = f.read()
f.close()

bf_code = []
bf_code = translate(source, bf_code)

elfLength = len(makeELF(bf_code))

mmap.restype = POINTER(ARRAY(c_ubyte, elfLength))
p = mmap(
    0, elfLength,
    PROT_READ | PROT_WRITE | PROT_EXEC,
    MAP_PRIVATE | MAP_ANONYMOUS,
    -1, 0
)[0]

#getaddr = CFUNCTYPE(c_void_p, c_void_p)(lambda p: p)
#f       = CFUNCTYPE(c_void_p)(getaddr(p))

#bf_code[3:11]   = conv64(getaddr(bf_mem))
###elf = makeELF(bf_code, getaddr(p))
elf = makeELF(bf_code)

# for debug
#print map(hex, bf_code)

# output ELF format file
p[:] = elf
with open('jit.out', "wb") as fp:
    fp.write(p)

munmap(p, len(elf))

