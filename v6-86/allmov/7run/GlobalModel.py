import re

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
        r = re.match('[a-f][hl]$', name)
        if r != None:
            cls.set8BitReg(r.group(), val)
        else:
            cls.reg[name] = val

    @classmethod
    def getReg(cls, name):
        r = re.match('[a-f][hl]$', name)
        if r != None:
            return cls.get8BitReg(r.group())
        else:
            return cls.reg[name]
        
    @classmethod
    def set8BitReg(cls, name, val):
        try:
            regName = name[0] + 'x'
            if name[1] == 'h':
                setVal = (cls.reg[regName] & 0x00ff) | (val << 8)
            else:
                setVal = (cls.reg[regName] & 0xff00) | val
            
            cls.reg[regName] = setVal
        except KeyError:
            cls.reg[regName] = 0
            cls.set8BitReg(name, val)
        
    @classmethod
    def get8BitReg(cls, name):
        regName = name[0] + 'x'
        if name[1] == 'h':
            return cls.reg[regName] >> 8
        else:
            return (cls.reg[regName] & 0x00ff)

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
