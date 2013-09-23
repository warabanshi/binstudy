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
        if convNum(text, 1) in [0xb8, 0xbb, 0xb9, 0xba, 0xbd, 0xbe, 0xbf, 0xbc]:
            mov = self.lazyLoad('Mov')
            self.pc += mov.execute(self.pc, text, convNum(text, 1))

        elif convNum(text, 1) in [0xb5, 0xb1]:
            mov = self.lazyLoad('Mov')
            self.pc += mov.execute(self.pc, text, convNum(text, 1))

        elif convNum(text, 2) in [0xc707, 0xc747, 0xc607, 0xc647, 0x8b26]:
            mov = self.lazyLoad('Mov')
            self.pc += mov.execute(self.pc, text, convNum(text, 2))

        elif convNum(text, 2) in [0x8907, 0x894f, 0x890f]:
            mov = self.lazyLoad('Mov')
            self.pc += mov.execute(self.pc, text, convNum(text, 2))

        elif convNum(text, 2) in [0x8807, 0x8867]:
            mov = self.lazyLoad('Mov')
            self.pc += mov.execute(self.pc, text, convNum(text, 2))

        elif convNum(text, 2) in [0xc706, 0xc606]:
            mov = self.lazyLoad('Mov')
            self.pc += mov.execute(self.pc, text, convNum(text, 2))

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
