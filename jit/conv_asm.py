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
            r.append('inc   rbx')

        elif s == '<':
            r.append('dec   rbx')

        elif s == '+':
            r.append('inc   byte ptr [rbx]')

        elif s == '-':
            r.append('dec   byte ptr [rbx]')

        elif s == '.':
            r.append('mov   rdi,    [rbx]')
            r.append('call  putchar')

        elif s == ',':
            r.append('call  getchar')
            r.append('mov   [rbx], rax')

        elif s == '[':
            loop_name = 'loop' + str(loop_label)
            loop_stack.append(loop_name)

            r.append('start_' + loop_name + ':')
            r.append('cmp   byte ptr [rbx], 0')
            r.append('jz    end_' + loop_name)

            loop_label += 1

        elif s == ']':
            loop_name = loop_stack.pop()
            r.append('jmp   start_' + loop_name)
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
