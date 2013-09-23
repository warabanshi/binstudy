from struct import *
from GlobalModel import GlobalModel as gm
from Utils import *
from mnemonic.Mnemonic import Mnemonic

class Mov(Mnemonic):

    @staticmethod
    def execute(pc, text, mnemonic):

        if  (mnemonic & 0xf8) == 0b10111000:    # mov immediate to register
            regList = ['ax', 'cx', 'dx', 'bx', 'sp', 'bp', 'si', 'di']
            key = mnemonic & 0b00000111
            val, = unpack('<H', text[1:3])
            Mov.printVal2Reg(pc, convNum(text, 3), regList[key], val)
            pcInc = 3

        elif (mnemonic & 0xfc) == & 0b110011:   # mov immediate to register/memory
            w = (mnemonic >> 24) & 1
            mod = (mnemonic >> 22) & 0b11
            r_div_m = (mnemonic >> 16) & 0b111
            regList = ['bx+si', 'bx+di', 'bp+si', 'bp+di', 'si', 'di', 'bp', 'bx']
            val, = unpack('<H', text[2:4])
            Mov.printVal2Ref(pc ,convNum(text, 4), regList[r_div_m], val)
            pcInc = 4

        elif mnemonic == 0xb5:  # mov ch, #NN
            val, = unpack('B', text[1])
            Mov.printVal2Reg(pc, convNum(text, 2), 'ch', val)
            pcInc = 2
        elif mnemonic == 0xb1:  # mov cl, #NN
            val, = unpack('B', text[1])
            Mov.printVal2Reg(pc, convNum(text, 2), 'cl', val)
            pcInc = 2
        elif mnemonic == 0x8b26: # mov sp, [NNNN]
            val, = unpack('<H', text[2:4])
            Mov.printMem2Reg(pc, convNum(text, 4), 'sp', val)
            pcInc = 4
        elif mnemonic == 0xc707: # mov [bx], #NNNN
            Mov.printVal2Reg(pc, convNum(text, 4), '[bx]', convNum(text[2:4], 2))
            pcInc = 4
        elif mnemonic == 0xc747: # mov [bx+x], #NNNN
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
        elif mnemonic == 0xc706: # mov [1234], #1234
            s = "[%04x]" % unpack('<H', text[2:4])
            Mov.printVal2Mem(pc, convNum(text, 6), s, convNum(text[4:6], 2))
            pcInc = 6
        elif mnemonic == 0xc606: # mov byte [1234], #12
            s = "byte [%04x]" % unpack('<H', text[2:4])
            Mov.printVal2Mem(pc, convNum(text, 5), s, convNum(text[4], 1))
            pcInc = 5
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

    @staticmethod
    def printVal2Mem(pc, raw, pos, val):
        inst = 'mov %s, %04x' % (pos, val)
        printInst(pc, raw, inst)

    @staticmethod
    def printMem2Reg(pc, raw, reg, pos):
        inst = 'mov %s, [%04x]' % (reg, pos)
        printInst(pc, raw, inst)

    def printVal2Ref(pc, raw, ref, val):
        inst = 'mov [%s], %0x4' % (ref, val)
        printInst(pc, raw, inst)


