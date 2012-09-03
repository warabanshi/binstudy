import sys

asm = []
asm.append('.intel_syntax noprefix')
asm.append('.comm mem, 30000')
asm.append('.globl main')
asm.append('')
asm.append('main:')
asm.append('lea     rbx, mem')

def translate(source, r):
    spos = 0    # source position
    loop_label = 0  # loop label
    loop_stack = []

    while True:
        s = source[spos]    # retrieve bf instruction

        if spos >= len(source) - 1:
            break

        elif s == '>':
            r.append(0x48)
            r.append(0xff)
            r.append(0xc3)

        elif s == '<':
            r.append(0x48)
            r.append(0xff)
            r.append(0xcb)

        elif s == '+':
            r.append(0xfe)
            r.append(0x03)

        elif s == '-':
            r.append(0xfe)
            r.append(0x0b)

        elif s == '.':
            r.append(0x48)
            r.append(0x8b)
            r.append(0x3b)
            r.append(0x41)
            r.append(0xff)
            r.append(0xd4)

        elif s == ',':
            r.append(0x41)
            r.append(0xff)
            r.append(0xd5)
            r.append(0x48)
            r.append(0x89)
            r.append(0x03)

        elif s == '[':
            loop_name = 'loop' + str(loop_label)
            loop_stack.append(loop_name)

            r.append('start_' + loop_name + ':')
            r.append(0x80)
            r.append(0x3b)
            r.append(0x00)
            r.append(0x74)
            r.append(0x02)

            loop_label += 1

        elif s == ']':
            loop_name = loop_stack.pop()
            r.append('jmp   start_' + loop_name)
            r.append(0xeb)
            r.append(0xf9)
            r.append('end_' + loop_name + ':')

        spos += 1
    
    return r

f = open(sys.argv[1])
source = f.read()
f.close()

asm = translate(source, asm)

f = open('asm.s', 'w')
f.write("\n".join(asm) + "\n")
f.close()
