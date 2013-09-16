from struct import *
from GlobalModel import GlobalModel as gm
from Utils import *
from mnemonic.Mnemonic import Mnemonic

class Sub(Mnemonic):

    @staticmethod
    def execute(pc, text, mnemonic):

        if mnemonic == 0x812e:      # sub [1234], #1234
            addr, = unpack('<H', text[2:4])
            val, = unpack('<H', text[4:6])
            Sub.subFromAddr(pc, addr, val, 2)
            pcInc = 6
        elif mnemonic == 0x802e:    # sub byte [1234], #12
            addr, = unpack('<H', text[2:4])
            val, = unpack('<B', text[4])
            Sub.subFromAddr(pc, addr, val, 1)
            pcInc = 5
        else:
            msg = "unknown register name specified: " + hex(mnemonic)
            raise Exception(msg)

        return pcInc
    
    @staticmethod
    def subFromAddr(pc, addr, val, byte):
        data = convNum(gm.getData(addr, byte), byte)

        if byte == 1:
            fmt = 'B'
        elif byte == 2:
            fmt = 'H'
        else:
            raise Exception("invalid byte num specified")

        gm.setData(addr, pack(fmt, (data - val)))

