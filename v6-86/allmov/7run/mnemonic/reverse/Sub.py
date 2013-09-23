from struct import *
from GlobalModel import GlobalModel as gm
from Utils import *
from mnemonic.Mnemonic import Mnemonic

class Sub(Mnemonic):

    @staticmethod
    def execute(pc, text, mnemonic):

        if mnemonic == 0x812e:    # sub [1234], #1234
            addr,  = unpack('<H', text[2:4])
            val, = unpack('<H', text[4:6])
            Sub.printInst(pc, convNum(text, 6), '['+hex(addr)+']', val)
            pcInc = 6
        elif mnemonic == 0x802e:    # sub byte [1234], #12
            addr,  = unpack('<H', text[2:4])
            val, = unpack('<B', text[4])
            Sub.printInst(pc, convNum(text, 5), '['+hex(addr)+']', val)
            pcInc = 5
        else:
            raise Exception("unknown register name specified")

        return pcInc
    
    @staticmethod
    def printInst(pc, raw, target, val):
        inst = 'sub %s, %04x' % (target, val)
        printInst(pc, raw, inst)

