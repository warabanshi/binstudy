from struct import *
from GlobalModel import GlobalModel as gm
from Utils import *
from nimonic.Nimonic import Nimonic

class Mov(Nimonic):

    @staticmethod
    def execute(pc, text, nimonic):

        if nimonic == 0xb8:
            val, = unpack('<H', text[1:3])
            Mov.mov2reg(pc, 'ax', val)
            pcInc = 3
        elif nimonic == 0xbb:
            val, = unpack('<H', text[1:3])
            Mov.mov2reg(pc, 'bx', val)
            pcInc = 3
        elif nimonic == 0xc707:
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
