from struct import *
from GlobalModel import GlobalModel as gm
from Utils import *
from mnemonic.Mnemonic import Mnemonic

class Mov(Mnemonic):

    @staticmethod
    def execute(pc, text, mnemonic):

        if mnemonic == 0xb8:        # mov ax, #1
            val, = unpack('<H', text[1:3])
            Mov.mov2reg(pc, 'ax', val)
            pcInc = 3
        elif mnemonic == 0xbb:      # mov bx, #1
            val, = unpack('<H', text[1:3])
            Mov.mov2reg(pc, 'bx', val)
            pcInc = 3
        elif mnemonic == 0xb9:      # mov cx, #1
            val, = unpack('<H', text[1:3])
            Mov.mov2reg(pc, 'cx', val)
            pcInc = 3
        elif mnemonic == 0xc707:    # mov [bx], #1234
            Mov.mov2derefer(pc, 'bx', text[2:4], 0)
            pcInc = 4
        elif mnemonic == 0xc747:    # mov [bx+x], #1234
            Mov.mov2derefer(pc, 'bx', text[3:5], convNum(text[2], 1))
            pcInc = 5
        elif mnemonic == 0xc607:    # mov ptr [bx], #12
            Mov.mov2derefer(pc, 'bx', text[2], 0)
            pcInc = 3
        elif mnemonic == 0xc647:    # mov ptr [bx+x], #12
            Mov.mov2derefer(pc, 'bx', text[3], convNum(text[2], 1))
            pcInc = 4
        elif mnemonic == 0x8907:    # mov [bx], ax
            Mov.mov2derefer(pc, 'bx', pack('<H', gm.getReg('ax')), 0)
            pcInc = 2
        elif mnemonic == 0x894f:    # mov [bx+x], cx
            Mov.mov2derefer(pc, 'bx', pack('<H', gm.getReg('cx')), convNum(text[2], 1))
            pcInc = 3
        else:
            raise "unknown register name specified"

        return pcInc
    
    @staticmethod
    def mov2reg(pc, regname, val):
        gm.setReg(regname, val)

    @staticmethod
    def mov2derefer(pc, regname, val, displace):
        addr = gm.getReg(regname)
        gm.setData(addr+displace, val)
