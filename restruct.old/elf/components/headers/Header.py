from elf.Utils import *

class Header(object):

    def __init__(self):
        self.contents = {}
        self.pos = 0

    def set(self, key, val):
        self.contents[key] = val

    def get(self, key):
        return self.contents[key]

    def resetPos(self, pos):
        self.pos = pos

    # bs: bytesize
    def fetch(self, bs, byteList):
        r = convBin(byteList[self.pos:self.pos+bs])
        self.pos += bs

        return r

    def getByte(self, byteList):
        return self.fetch(1, byteList)

    def getWord(self, byteList):
        return self.fetch(2, byteList)

    def getDw(self, byteList):
        return self.fetch(4, byteList)

    def getQw(self, byteList):
        return self.fetch(8, byteList)

    def retrieve(self):
        raise('method retrieve() has to implement individualy')
