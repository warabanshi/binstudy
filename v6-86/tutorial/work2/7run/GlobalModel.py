class GlobalModel(object):

    reverseFlag = False
    textlen = 0         # text section length
    alldata = None      # all data that include .text and .data
    reg = {
        'ax': None
    }

    @classmethod
    def setReverse(cls):
        cls.reverseFlag = True

    @classmethod
    def isReverse(cls):
        return cls.reverseFlag

    @classmethod
    def setReg(cls, name, val):
        cls.reg[name] = val

    @classmethod
    def getReg(cls, name):
        return cls.reg[name]

    @classmethod
    def initData(cls, textlen, alldata):
        cls.textlen = textlen
        cls.alldata = alldata

    @classmethod
    def setData(cls, offset, data):
        if offset < cls.textlen:
            raise Exception("can't rewrite .text area")

        tail = offset + len(data)
        cls.alldata = cls.alldata[:offset] + data + cls.alldata[tail:]

    @classmethod
    def getData(cls, offset, length):
        tail = offset + length
        return cls.alldata[offset:tail]
