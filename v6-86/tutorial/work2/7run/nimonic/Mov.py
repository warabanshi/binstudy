from struct import *
from GlobalModel import GlobalModel as gm
from Utils import *

class Mov(object):

    @staticmethod
    def execute(pc, text, nimonic):

        if nimonic == 0xb8:
            val, = unpack('<H', text[1:3])
            if gm.isReverse():
                Mov.printReverse(pc, convNum(text, 3), 'ax', val)
            else:
                Mov.mov2reg(pc, 'ax', val)
            pcInc = 3
        elif nimonic == 0xbb:
            val, = unpack('<H', text[1:3])
            if gm.isReverse():
                Mov.printReverse(pc, convNum(text, 3), 'bx', val)
            else:
                Mov.mov2reg(pc, 'bx', val)
            pcInc = 3
        elif nimonic == 0xc707:
            if gm.isReverse():
                Mov.printReverse(pc, convNum(text, 4), '[bx]', convNum(text[2:4], 2))
            else:
                Mov.mov2derefer(pc, 'bx', text[2:4])
            pcInc = 4
        else:
            raise "unknown register name specified"

        return pcInc
    
    @staticmethod
    def mov2reg(pc, regname, val):
        gm.setReg(regname, val)

    @staticmethod
    def mov2derefer(pc, regname, val):
        addr = gm.getReg(regname)
        gm.setData(addr, val)

    @staticmethod
    def printReverse(pc, raw, regname, val):
        inst = 'mov %s %04x' % (regname, val)
        printInst(pc, raw, inst)
