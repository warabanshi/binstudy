from struct import *
from GlobalModel import GlobalModel as gm
from Utils import *
from mnemonic.Mnemonic import Mnemonic

class Mov(Mnemonic):

    regname = ['ax', 'cx', 'dx', 'bx', 'sp', 'bp', 'si', 'di']

    @classmethod
    def execute(cls, pc, text, instByte):

        if   0x88 <= instByte <= 0x8b:  # mov register/memory to/from register
            None    # implement later

        elif 0xc6 <= instByte <= 0xc7:   # mov immediate to register/memory
            w   = instByte & 0b1
            val, = unpack('B', text[1])

            mode = (0b11000000 & val) >> 6
            r_m = (0b111 & val)

            disp = 0
            if mode == 0b00:
                if r_m == 0b110:
                    disp, data = unpack('<HH', text[2:6])
                    pcInc = 6
                else:
                    data, = unpack('<H', text[2:4])
                    pcInc = 4
            elif mode == 0b01:
                disp, data = unpack('<bH', text[2:5])
                pcInc = 5
            elif mode == 0b10:
                disp, data = unpack('<HH', text[2:6])
                pcInc = 6
            elif mode == 0b11:
                data, = unpack('<H', text[2:4])
                pcInc = 4

            target = '[' + cls.getRegWithDisp(r_m, mode, disp) + ']'

            Mov.printVal2Reg(pc, convNum(text, pcInc), target, data)


        elif 0xb0 <= instByte <= 0xbf:   # mov immediate to register
            w   = (instByte & 0b00001000) >> 3
            key = instByte & 0b00000111
            if w == 1:
                data, = unpack('<H', text[1:3])
                pcInc = 3
            else:
                data, = unpack('B', text[1])
                pcInc = 2

            Mov.printVal2Reg(pc, convNum(text, pcInc), cls.regname[key], data)


            '''
        elif (mnemonic & 0xfc) == & 0b110011:   # mov immediate to register/memory
            w = (mnemonic >> 24) & 1
            mod = (mnemonic >> 22) & 0b11
            r_div_m = (mnemonic >> 16) & 0b111
            regList = ['bx+si', 'bx+di', 'bp+si', 'bp+di', 'si', 'di', 'bp', 'bx']
            val, = unpack('<H', text[2:4])
            Mov.printVal2Ref(pc ,convNum(text, 4), regList[r_div_m], val)
            pcInc = 4

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

        elif instByte == 0xb5:  # mov ch, #12
            val, = unpack('B', text[1])
            Mov.printVal2Reg(pc, convNum(text, 2), 'ch', val)
            pcInc = 2
        elif instByte == 0xb1:  # mov cl, #12
            val, = unpack('B', text[1])
            Mov.printVal2Reg(pc, convNum(text, 2), 'cl', val)
            pcInc = 2
            '''
        elif instByte == 0xc707: # mov [bx], #1324
            Mov.printVal2Reg(pc, convNum(text, 4), '[bx]', convNum(text[2:4], 2))
            pcInc = 4
        elif instByte == 0xc747: # mov [bx+x], #1234
            displace = str(convNum(text[2], 1))
            Mov.printVal2Reg(
                pc, convNum(text, 5), '[bx+'+displace+']', convNum(text[3:5], 2)
            )
            pcInc = 5
        elif instByte == 0xc607: # mov ptr [bx], #12
            Mov.printVal2Reg(pc, convNum(text, 3), 'byte [bx]', convNum(text[2], 1))
            pcInc = 3
        elif instByte == 0xc647: # mov ptr [bx+x], #12
            displace = str(convNum(text[2], 1))
            Mov.printVal2Reg(
                pc, convNum(text, 4), 'byte [bx+'+displace+']', convNum(text[3], 1)
            )
            pcInc = 4
        elif instByte == 0x8907: # mov [bx], ax
            Mov.printReg2Reg(pc, convNum(text, 2), '[bx]', 'ax')
            pcInc = 2
        elif instByte == 0x8807: # mov [bx], al
            Mov.printReg2Reg(pc, convNum(text, 2), '[bx]', 'al')
            pcInc = 2
        elif instByte == 0x8867: # mov [bx+x], ah
            displace = str(convNum(text[2], 1))
            Mov.printReg2Reg(
                pc, convNum(text, 3), '[bx+'+displace+']', 'ah'
            )
            pcInc = 3
        elif instByte == 0x890f: # mov [bx], cx
            Mov.printReg2Reg(pc, convNum(text, 2), '[bx]', 'cx')
            pcInc = 2
        elif instByte == 0x894f: # mov [bx+x], cx
            displace = str(convNum(text[2], 1))
            Mov.printReg2Reg(
                pc, convNum(text, 3), '[bx+'+displace+']', 'cx'
            )
            pcInc = 3
        elif instByte == 0xc706: # mov [1234], #1234
            s = "[%04x]" % unpack('<H', text[2:4])
            Mov.printVal2Mem(pc, convNum(text, 6), s, convNum(text[4:6], 2))
            pcInc = 6
        elif instByte == 0xc606: # mov byte [1234], #12
            s = "byte [%04x]" % unpack('<H', text[2:4])
            Mov.printVal2Mem(pc, convNum(text, 5), s, convNum(text[4], 1))
            pcInc = 5
        else:
            raise Exception("unknown register name specified")

        return pcInc

    @classmethod
    def getRegWithDisp(cls, r_m, mode, disp):   # get register name with displacement
        if disp > 0:
            dispstr = '+' + hex(disp)
        elif disp < 0:
            dispstr = hex(disp)
        else:
            dispstr = ''

        if r_m == 0b000:
            return 'bx+si' + dispstr
        elif r_m == 0b001:
            return 'bx+di' + dispstr
        elif r_m == 0b010:
            return 'bp+si' + dispstr
        elif r_m == 0b011:
            return 'bp+di' + dispstr
        elif r_m == 0b100:
            return 'si' + dispstr
        elif r_m == 0b101:
            return 'di' + dispstr
        elif r_m == 0b110:
            if mode == 0b00:
                return dispstr
            else:
                return 'bp' + dispstr
        elif r_m == 0b111:
            return 'bx' + dispstr
    
    @classmethod
    def printVal2Reg(cls, pc, raw, reg, val):
        inst = 'mov %s, %04x' % (reg, val)
        printInst(pc, raw, inst)

    @classmethod
    def printReg2Reg(cls, pc, raw, reg1, reg2):
        inst = 'mov %s, %s' % (reg1, reg2)
        printInst(pc, raw, inst)

    @classmethod
    def printVal2Mem(cls, pc, raw, pos, val):
        inst = 'mov %s, %04x' % (pos, val)
        printInst(pc, raw, inst)
