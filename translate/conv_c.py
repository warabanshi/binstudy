import sys

head = []
core = []
init = []

head.append('#include <stdio.h>')
head.append('#include <string.h>')
head.append('#include <stdlib.h>')

init.append('char* init() {')
init.append('int length = 100;')
init.append('int i;')
init.append('char input[length];')
init.append('char* mem = (char*)malloc(length);')
init.append('if (mem == NULL) { printf("cant allocate memory"); }')
init.append('for (i = 0; i < length; i++) { mem[i] = 0x0; }')
init.append('return mem;')
init.append('}')

def translate(source, core):
    sourcePos = 0

    while True:
        statement = source[sourcePos]

        if sourcePos >= len(source) - 1:
            break

        if statement == '>':
            core.append('mem++;')

        elif statement == '<':
            core.append('mem--;')

        elif statement == '+':
            core.append('(*mem)++;')

        elif statement == '-':
            core.append('(*mem)--;')

        elif statement == '.':
            core.append('putchar(*mem);')

        elif statement == ',':
            core.append('*mem = getchar();')

        elif statement == '[':
            core.append('while(*mem) {')

        elif statement == ']':
            core.append('}')

        sourcePos += 1

    return core

f = open(sys.argv[1])
source = f.read()
f.close()

core.append('int main(argc, argv) {')
core.append('char* mem = init();')
core = translate(source, core)
core.append('}')

f = open('transed.c', 'w')
f.write("\n".join(head) + "\n\n")
f.write("\n".join(init) + "\n\n")
f.write("\n".join(core) + "\n\n")
f.close()
