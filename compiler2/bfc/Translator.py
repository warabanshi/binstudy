import sys, struct

class Translator(object):

    def __init__(self):
        self.funcList = []  # dummy address list
        self.addrList = []  # dummy address list
        self.text = ''

    def addFuncList(self, offset, size, purpose):
        self.funcList.append( (offset, size, purpose) )

    def getFuncList(self):
        return self.funcList

    def addAddrList(self, offset, size, purpose):
        self.addrList.append( (offset, size, purpose) )

    def getAddrList(self):
        return self.addrList

    def getText(self):
        return self.text

    def translate(self, source):
        idxStack = []   # stack list index for loop

        sourceList = list(source)

        r = [] # result
        # mov  rbx, 0x0000000000000000  (set .bss address later)
        r += [0x48, 0xbb]
        self.addAddrList(len(r), 8, '.bss')
        r += [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

        for s in sourceList:

            if s == '>':
                # inc   rbx
                r += [0x48, 0xff, 0xc3]

            elif s == '<':
                # dec   rbx
                r += [0x48, 0xff, 0xcb]

            elif s == '+':
                # inc   byte ptr [rbx]
                r += [0xfe, 0x03]

            elif s == '-':
                # dec   byte ptr [rbx]
                r += [0xfe, 0x0b]

            elif s == '.':
                # mov   rdi, [rbx]
                r += [0x48, 0x8b, 0x3b]
                # call putchar (set when do linking)
                #  -> set address offset from here
                r += [0xe8, 0x00, 0x00, 0x00, 0x00]
                self.addFuncList(len(r)-4, 4, 'putchar')

            elif s == ',':
                # call getchar (set when do linking)
                #  -> set address offset from here
                r += [0xe8, 0x00, 0x00, 0x00, 0x00]
                self.addFuncList(len(r)-4, 4, 'getchar')
                # mov   [rbx], rax
                r += [0x48, 0x89, 0x03]

            elif s == '[':
                # start_(loop_name):
                # cmp   byte ptr [rbx], 0
                # jz    dword end_(loop_name)
                idxStack.append(len(r))
                r += [0x80, 0x3b, 0x00]
                r += [0x0f, 0x84, 0x00, 0x00, 0x00, 0x00]

            elif s == ']':
                # jmp   dword start_(loop_name)
                # end_(loop_name):
                r += [0xe9, 0x00, 0x00, 0x00, 0x00]
                idx = len(r)
                loop_index = idxStack.pop()

                # set offset of jump address which is start of loop
                backOffset = loop_index - idx
                r[idx-4:idx] = struct.unpack('4B', struct.pack('<i', backOffset))

                # set offset of jump address which is after loop
                forwardOffset = idx - (loop_index + 9)
                r[loop_index+5:loop_index+9] = struct.unpack('4B', struct.pack('<i', forwardOffset))

        # exit system call
        r += [0xb8, 0x3c, 0x00, 0x00, 0x00]
        r += [0xbf, 0x2a, 0x00, 0x00, 0x00]
        r += [0x0f, 0x05]

        self.text = struct.pack(str(len(r))+'B', *r)
