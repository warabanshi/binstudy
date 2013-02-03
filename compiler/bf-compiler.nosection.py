import sys, struct
from ctypes import *

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
    e.extend([0x02, 0x00])                  # u16 e_phnum
    e.extend([0x00, 0x00])                  # u16 e_shentsize
    e.extend([0x00, 0x00])                  # u16 e_shnum
    e.extend([0x00, 0x00])                  # u16 e_shstrndx

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
    phsize = len(p)

    # program header for .bss
    p.extend([0x01, 0x00, 0x00, 0x00])      # u32 p_type
    p.extend([0x06, 0x00, 0x00, 0x00])      # u32 p_flags
    p.extend([0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # u64 p_offset
    p.extend([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # u64 p_vaddr
    p.extend([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # u64 p_paddr
    p.extend([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # u64 p_filesz
    p.extend([0x30, 0x75, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # u64 p_memsz
    p.extend([0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00])  # u64 p_align


    filesize = len(e + p + bf)

    e[24:32] = conv64(addr + len(e + p))    # set e_entry
    e[32:40] = conv64(len(e))               # set e_phoff
    e[52:54] = conv16(len(e))               # set e_ehsize
    e[54:56] = conv16(phsize)               # set e_phentisize

    p[16:24] = conv64(addr)                 # set p_vaddr
    p[24:32] = conv64(addr)                 # set p_paddr
    p[32:40] = conv64(filesize)             # set p_filesz
    p[40:48] = conv64(filesize)             # set p_memsz
    #p[48:56] = conv64(addr + len(e))       # set p_align

    p[72:80] = conv64(addr + 0x200000)      # set p_vaddr
    p[80:88] = conv64(addr + 0x200000)      # set p_paddr

    bf[2:10]   = conv64(0x08248000)

    return e + p + bf

def translate(source, r):
    spos        = 0

    loop_index_stack    = []
    jmp_index_stack   = []
    back_index_stack  = []

    # initialize
    # mov  rbx, 0x0000000000000000  (set .bss address later)
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
            r.extend([0xbf, 0x00, 0x00, 0x00, 0x00])
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

    # exit system call
    r.extend([0xb8, 0x3c, 0x00, 0x00, 0x00])
    r.extend([0xbf, 0x2a, 0x00, 0x00, 0x00])
    r.extend([0x0f, 0x05])

    return r

f = open(sys.argv[1])
source = f.read()
f.close()

bf_code = []
bf_code = translate(source, bf_code)

elf = makeELF(bf_code)
elfLength = len(elf)

# output ELF format file
p = (c_ubyte* elfLength)()
p[:] = elf
with open('elf.out', "wb") as fp:
    fp.write(p)

