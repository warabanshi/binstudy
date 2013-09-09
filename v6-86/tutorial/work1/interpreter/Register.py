class Register(object):

    reg = {
        'ax': None
    }

    @classmethod
    def setReg(cls, name, val):
        cls.reg[name] = val

    @classmethod
    def getReg(cls, name):
        return cls.reg[name]
