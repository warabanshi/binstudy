import sys

from struct import unpack
from Utils import *
from nimonic.Mov import Mov as mov
from nimonic.Interrupt import Interrupt as intrpt

class Interpreter(object):
    
    pc = 0
    text = ''

    def __init__(self):
        None

    def execute(self):
        f = open("a.out", "rb")
        header = f.read(16)
        tsize, dsize = unpack('<HH', header[2:6])

        self.text = f.read(tsize+dsize)
        while self.pc < len(self.text):
            self.interpret(self.text[self.pc:])

    def interpret(self, text):
        if convNum(text, 1) == 0xb8:
            self.pc += mov.execute(self.pc, text)

        elif convNum(text, 1) == 0xcd:
            self.pc += intrpt.execute(self.pc, text)

        else:
            self.pc += 1

interp = Interpreter()
interp.execute()
