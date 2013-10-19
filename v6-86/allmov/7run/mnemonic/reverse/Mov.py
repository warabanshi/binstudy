from struct import *
from GlobalModel import GlobalModel as gm
from Utils import *
from mnemonic.Mnemonic import Mnemonic

class Mov(Mnemonic):

    regname = ['ax', 'cx', 'dx', 'bx', 'sp', 'bp', 'si', 'di']
    reg8bit = ['al', 'cl', 'dl', 'bl', 'ah', 'ch', 'dh', 'bh']

    @classmethod
    def execute(cls, pc, text, instByte):

        if   0x88 <= instByte <= 0x8b:  # mov register/memory to/from register
            d   = (instByte & 0b10) >> 1
            w   = instByte & 0b01
            val, = unpack('B', text[1])
            pcInc = 2

            mode = (0b11000000 & val) >> 6
            reg = (0b111000 & val) >> 3
            r_m = (0b111 & val)

            disp = 0
            if mode == 0b00:
                if r_m == 0b110:
                    disp, = unpack('<H', text[2:4])
                    pcInc += 2
            elif mode == 0b01:
                disp, = unpack('<b', text[2])
                pcInc += 1
            elif mode == 0b10:
                disp, = unpack('<H', text[2:4])
                pcInc += 2
            elif mode == 0b11:
                None

            if mode == 0b11:
                r_mStr = cls.regname[r_m]
            else:
                r_mStr = '[' + cls.getRegWithDisp(r_m, mode, disp) + ']'

            if d == 1:      # d = 1 then "to" reg
                valTo = cls.regname[reg]
                valFrom = r_mStr
            else:
                valTo = r_mStr
                valFrom = cls.regname[reg]

            Mov.printReg2Reg(pc, convNum(text, pcInc), valTo, valFrom)

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
            reg = instByte & 0b00000111
            if w == 1:
                data, = unpack('<H', text[1:3])
                pcInc = 3
            else:
                data, = unpack('B', text[1])
                pcInc = 2

            Mov.printVal2Reg(pc, convNum(text, pcInc), cls.regname[reg], data)

        elif 0xa0 <= instByte <= 0xa1:  # mov memory to accumulator
            w = instByte & 0b1

            if w == 1:
                addr, = unpack('<H', text[1:3])
            else:
                absent, addr = unpack('BB', text[1:3])
            pcInc = 3
            
            Mov.printReg2Reg(
                pc, convNum(text, pcInc), cls.regname[0], '['+hex(addr)+']'
            )

        elif 0xa2 <= instByte <= 0xa3:  # mov accumulator to memory
            w = instByte & 0b1
            addr, = unpack('<H', text[1:3])
            if w == 1:
                addr, = unpack('<H', text[1:3])
            else:
                absent, addr = unpack('BB', text[1:3])
            pcInc = 3
            
            Mov.printReg2Reg(
                pc, convNum(text, pcInc), '['+hex(addr)+']', cls.regname[0]
            )

        elif instByte == 0x8e:          # mov register/memory to SegmentRegister
            None

        elif instByte == 0x8c:          # mov SegmentRegister to register/memory
            None

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
