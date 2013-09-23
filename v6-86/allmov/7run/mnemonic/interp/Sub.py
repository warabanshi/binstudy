from struct import *
from GlobalModel import GlobalModel as gm
from Utils import *
from mnemonic.Mnemonic import Mnemonic

class Sub(Mnemonic):

    @staticmethod
    def execute(pc, text, mnemonic):

        if mnemonic == 0x812e:      # sub [1234], #1234
            addr, val = unpack('<HH', text[2:6])
            Sub.subFromAddr(pc, addr, val, '<H',  2)
            pcInc = 6
        elif mnemonic == 0x802e:    # sub byte [1234], #12
            addr, val = unpack('<HB', text[2:5])
            Sub.subFromAddr(pc, addr, val, 'B', 1)
            pcInc = 5
        else:
            msg = "unknown register name specified: " + hex(mnemonic)
            raise Exception(msg)

        return pcInc
    
    @staticmethod
    def subFromAddr(pc, addr, val, fmt, byte):
        baseVal, = unpack(fmt, gm.getData(addr, byte))
        result = baseVal - val
        gm.setData(addr, pack(fmt, result))

