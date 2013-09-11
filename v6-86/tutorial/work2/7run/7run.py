import sys
from struct import unpack

from GlobalModel import *
from Utils import *
#from nimonic.Mov import Mov as mov
#from nimonic.Interrupt import Interrupt as intrpt

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
        if convNum(text, 1) in [0xb8, 0xbb]:
            mov = self.lazyLoad('Mov')
            self.pc += mov.execute(self.pc, text, convNum(text, 1))

        elif convNum(text, 2) in [0xc707]:
            mov = self.lazyLoad('Mov')
            self.pc += mov.execute(self.pc, text, convNum(text, 2))

        elif convNum(text, 1) == 0xcd:
            intrpt = self.lazyLoad('Interrupt')
            self.pc += intrpt.execute(self.pc, text)

        else:
            self.pc += 1

    def lazyLoad(self, name):
        if GlobalModel.isReverse():
            path = 'nimonic.reverse.' + name
        else:
            path = 'nimonic.interp.' + name

        try:
            mod = __import__(path)
        except: 
            raise Exception("module import failed: " + path)

        components = path.split('.')
        for comp in components[1:]:
            mod = getattr(mod, comp)

        return getattr(mod, name)

run7 = run7()
run7.execute()
