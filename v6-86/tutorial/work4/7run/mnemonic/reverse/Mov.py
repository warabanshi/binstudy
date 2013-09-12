from struct import *
from GlobalModel import GlobalModel as gm
from Utils import *
from mnemonic.Mnemonic import Mnemonic

class Mov(Mnemonic):

    @staticmethod
    def execute(pc, text, mnemonic):

        if mnemonic == 0xb8:    # mov ax, #1
            val, = unpack('<H', text[1:3])
            Mov.printReverse(pc, convNum(text, 3), 'ax', val)
            pcInc = 3
        elif mnemonic == 0xbb:  # mov bx, #1
            val, = unpack('<H', text[1:3])
            Mov.printReverse(pc, convNum(text, 3), 'bx', val)
            pcInc = 3
        elif mnemonic == 0xc707: # mov [bx], #1324
            Mov.printReverse(pc, convNum(text, 4), '[bx]', convNum(text[2:4], 2))
            pcInc = 4
        elif mnemonic == 0xc747: # mov [bx+x], #1234
            displace = str(convNum(text[2], 1))
            Mov.printReverse(
                pc, convNum(text, 5), '[bx+'+displace+']', convNum(text[3:5], 2)
            )
            pcInc = 5
        elif mnemonic == 0xc607: # mov ptr [bx], #12
            Mov.printReverse(pc, convNum(text, 3), 'byte [bx]', convNum(text[2], 1))
            pcInc = 3
        elif mnemonic == 0xc647: # mov ptr [bx+x], #12
            displace = str(convNum(text[2], 1))
            Mov.printReverse(
                pc, convNum(text, 4), 'byte [bx+'+displace+']', convNum(text[3], 1)
            )
            pcInc = 4
        else:
            raise Exception("unknown register name specified")

        return pcInc
    
    @staticmethod
    def printReverse(pc, raw, regname, val):
        inst = 'mov %s, %04x' % (regname, val)
        printInst(pc, raw, inst)
