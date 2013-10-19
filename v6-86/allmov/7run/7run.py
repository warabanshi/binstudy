import sys
from struct import unpack

from GlobalModel import *
from Utils import *

class run7(object):
    
    pc = 0
    text = ''

    def execute(self):
        argv = sys.argv
        if len(argv) == 2 and argv[1] == '-d':
            GlobalModel.setReverse()

        f = open("a.out", "rb")
        header = f.read(16)
        tsize, dsize = unpack('<HH', header[2:6])

        self.text = f.read(tsize)
        GlobalModel.initData(len(self.text), self.text + f.read(dsize))

        while self.pc < len(self.text):
            self.interpret(self.text[self.pc:])

    def interpret(self, text):

        firstByte, = unpack('B', text[0])

        mov     = self.lazyLoad('Mov')
        intrpt  = self.lazyLoad('Interrupt')
        sub     = self.lazyLoad('Sub')

        if (
            0x88 <= firstByte <= 0x8b or     # mov register/memory to/from register
            0xb0 <= firstByte <= 0xbf or     # mov immediate to register
            0xc6 <= firstByte <= 0xc7 or     # mov immediate to register/memory
            0xa0 <= firstByte <= 0xa1 or     # mov memory to accumulator
            0xa2 <= firstByte <= 0xa3 or     # mov accumulator to memory
            0x8e == firstByte or 0x8c == firstByte
        ):
            self.pc += mov.execute(self.pc, text, firstByte)

        elif convNum(text, 1) == 0xcd:
            intrpt = self.lazyLoad('Interrupt')
            self.pc += intrpt.execute(self.pc, text)

        elif convNum(text, 2) in [0x812e, 0x802e]:
            sub = self.lazyLoad('Sub')
            self.pc += sub.execute(self.pc, text, convNum(text, 2))

        else:
            self.pc += 1

    def lazyLoad(self, name):
        if GlobalModel.isReverse():
            path = 'mnemonic.reverse.' + name
        else:
            path = 'mnemonic.interp.' + name

        try:
            mod = __import__(path)
        except: 
            msg = "module import failed: " + path
            raise Exception(msg)

        components = path.split('.')
        for comp in components[1:]:
            mod = getattr(mod, comp)

        return getattr(mod, name)

run7 = run7()
run7.execute()
