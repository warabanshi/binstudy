from elf.Utils import *

class Header(object):

    def __init__(self):
        self.contents = {}
        self.keyEntry = {}
        self.pos = 0
        self.binList = []

    def set(self, key, val):
        self.contents[key] = val

    def get(self, key):
        return self.contents[key]

    def setPos(self, pos):
        self.pos = pos

    def setBinList(self, binList):
        self.binList = binList

    def clearBinList(self):
        self.binList = []

    # bs: bytesize
    def fetch(self, bs, key = None):
        r = convBin(self.binList[self.pos:self.pos+bs])
        self.pos += bs
        if key != None:
            self.keyEntry[key] = r

        return r

    def getByte(self, key = None):
        return self.fetch(1, key)

    def getWord(self, key = None):
        return self.fetch(2, key)

    def getDw(self, key = None):
        return self.fetch(4, key)

    def getQw(self, key = None):
        return self.fetch(8, key)

    #def getRange(self, start, size):
    #    return self.binList[start:start+size]

    def retrieve(self):
        raise('method retrieve() has to implement individualy')
