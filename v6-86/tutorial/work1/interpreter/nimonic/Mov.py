from Register import Register as reg

class Mov(object):

    @staticmethod
    def execute(pc, txt):
        nimonic, val, register = map(ord, txt[0:3])

        if register == 0x00:
            regname = 'ax'
        else:
            raise "unknown register name specified"

        pcInc = 3

        reg.setReg(regname, val)

        return pcInc
