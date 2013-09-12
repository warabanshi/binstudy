from struct import *
from GlobalModel import GlobalModel as gm
from Utils import *
from mnemonic.Mnemonic import Mnemonic

class Mov(Mnemonic):

    @staticmethod
    def execute(pc, text, mnemonic):

        if mnemonic == 0xb8:    # mov ax, #1
            val, = unpack('<H', text[1:3])
            Mov.printVal2Reg(pc, convNum(text, 3), 'ax', val)
            pcInc = 3
        elif mnemonic == 0xbb:  # mov bx, #1
            val, = unpack('<H', text[1:3])
            Mov.printVal2Reg(pc, convNum(text, 3), 'bx', val)
            pcInc = 3
        elif mnemonic == 0xb9:  # mov cx, #1
            val, = unpack('<H', text[1:3])
            Mov.printVal2Reg(pc, convNum(text, 3), 'cx', val)
            pcInc = 3
        elif mnemonic == 0xb5:  # mov ch, #12
            val, = unpack('B', text[1])
            Mov.printVal2Reg(pc, convNum(text, 2), 'ch', val)
            pcInc = 2
        elif mnemonic == 0xb1:  # mov cl, #12
            val, = unpack('B', text[1])
            Mov.printVal2Reg(pc, convNum(text, 2), 'cl', val)
            pcInc = 2
        elif mnemonic == 0xc707: # mov [bx], #1324
            Mov.printVal2Reg(pc, convNum(text, 4), '[bx]', convNum(text[2:4], 2))
            pcInc = 4
        elif mnemonic == 0xc747: # mov [bx+x], #1234
            displace = str(convNum(text[2], 1))
            Mov.printVal2Reg(
                pc, convNum(text, 5), '[bx+'+displace+']', convNum(text[3:5], 2)
            )
            pcInc = 5
        elif mnemonic == 0xc607: # mov ptr [bx], #12
            Mov.printVal2Reg(pc, convNum(text, 3), 'byte [bx]', convNum(text[2], 1))
            pcInc = 3
        elif mnemonic == 0xc647: # mov ptr [bx+x], #12
            displace = str(convNum(text[2], 1))
            Mov.printVal2Reg(
                pc, convNum(text, 4), 'byte [bx+'+displace+']', convNum(text[3], 1)
            )
            pcInc = 4
        elif mnemonic == 0x8907: # mov [bx], ax
            Mov.printReg2Reg(pc, convNum(text, 2), '[bx]', 'ax')
            pcInc = 2
        elif mnemonic == 0x8807: # mov [bx], al
            Mov.printReg2Reg(pc, convNum(text, 2), '[bx]', 'al')
            pcInc = 2
        elif mnemonic == 0x8867: # mov [bx+x], ah
            displace = str(convNum(text[2], 1))
            Mov.printReg2Reg(
                pc, convNum(text, 3), '[bx+'+displace+']', 'ah'
            )
            pcInc = 3
        elif mnemonic == 0x890f: # mov [bx], cx
            Mov.printReg2Reg(pc, convNum(text, 2), '[bx]', 'cx')
            pcInc = 2
        elif mnemonic == 0x894f: # mov [bx+x], cx
            displace = str(convNum(text[2], 1))
            Mov.printReg2Reg(
                pc, convNum(text, 3), '[bx+'+displace+']', 'cx'
            )
            pcInc = 3
        else:
            raise Exception("unknown register name specified")

        return pcInc
    
    @staticmethod
    def printVal2Reg(pc, raw, reg, val):
        inst = 'mov %s, %04x' % (reg, val)
        printInst(pc, raw, inst)

    @staticmethod
    def printReg2Reg(pc, raw, reg1, reg2):
        inst = 'mov %s, %s' % (reg1, reg2)
        printInst(pc, raw, inst)
