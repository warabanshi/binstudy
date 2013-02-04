class Header(object):

    def __init__(self, binList):
        self.contents = {}
        self.keyEntry = {}
        self.pos = 0
        self.binList = binList

    def set(self, key, val):
        self.contents[key] = val

    def get(self, key):
        return self.contents[key]

    def setPos(self, pos):
        self.pos = pos

    # argument list expected in little endien
    def convBin(self, l):
        b = 0
        for byte in reversed(l):
            b = (b << 8) | byte

        return b

    # bs: bytesize
    def fetch(self, bs, key = None):
        r = self.convBin(self.binList[self.pos:self.pos+bs])
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

    def getRange(self, start, size):
        return self.binList[start:start+size]

    def retrieve(self):
        raise('method retrieve() has to implement individualy')
