from struct import *
from GlobalModel import GlobalModel as gm
from Utils import *
from nimonic.Nimonic import Nimonic

class Mov(Nimonic):

    @staticmethod
    def execute(pc, text, nimonic):

        if nimonic == 0xb8:
            val, = unpack('<H', text[1:3])
            Mov.printReverse(pc, convNum(text, 3), 'ax', val)
            pcInc = 3
        elif nimonic == 0xbb:
            val, = unpack('<H', text[1:3])
            Mov.printReverse(pc, convNum(text, 3), 'bx', val)
            pcInc = 3
        elif nimonic == 0xc707:
            Mov.printReverse(pc, convNum(text, 4), '[bx]', convNum(text[2:4], 2))
            pcInc = 4
        else:
            raise "unknown register name specified"

        return pcInc
    
    @staticmethod
    def printReverse(pc, raw, regname, val):
        inst = 'mov %s %04x' % (regname, val)
        printInst(pc, raw, inst)
