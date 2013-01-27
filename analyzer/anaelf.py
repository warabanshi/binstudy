'''
ELF analyzer for x86-64
'''

import sys, struct

f = open(sys.argv[1])
binList = map(lambda x: int(ord(x)), f.read())

class ElfAnalyzer:
    pos = 0
    binList = []
    keyEntry = {}

    def __init__(self, binList):
        self.binList = binList
        pass

    def setPos(self, pos):
        self.pos = pos

    # argument list expected in little endien
    def makeBin(self, l):
        b = 0
        for byte in reversed(l):
            b = (b << 8) | byte

        return b

    def getKeyEntry(self, key):
        return self.keyEntry[key]

    def getRange(self, start, size):
        return self.binList[start:start+size]

    def getMagic(self):
        self.pos += 16
        return '/'.join(map(hex, self.binList[0:16]))

    # bs: bytesize
    def fetch(self, bs, key = None):
        r = self.makeBin(self.binList[self.pos:self.pos+bs])
        self.pos += bs
        if key != None:
            self.keyEntry[key] = r
        return r

    # key: specify the key for self.keyEntry if you want keeping retrieved value
    def getByte(self, key = None):
        return self.fetch(1, key)

    def getWord(self, key = None):
        return self.fetch(2, key)

    def getDw(self, key = None):
        return self.fetch(4, key)

    def getQw(self, key = None):
        return self.fetch(8, key)

ana = ElfAnalyzer(binList)
print('Magic            : %s' % ana.getMagic())
print('Type             : %s' % ana.getWord())
print('Machine          : %s' % ana.getWord())
print('Version          : %s' % ana.getDw())
print('EntryAddr        : %s' % ana.getQw())
print('ph-offset        : %s' % ana.getQw())
print('sh-offset        : %s' % ana.getQw('sh-offset'))
print('flags            : %s' % ana.getDw())
print('ELF-header size  : %s' % ana.getWord())
print('prg-header size  : %s' % ana.getWord('phsize'))
print('prg-header num   : %s' % ana.getWord('phnum'))
print('sct-haeder size  : %s' % ana.getWord('shsize'))
print('sct-haeder num   : %s' % ana.getWord('shnum'))
print('string section idx: %s' % ana.getWord('str-section-index'))

print("\n ------------- program header ------------- \n")
for i in range(ana.getKeyEntry('phnum')):
    print(" ----- program header : %d ----- " % ((i+1)))
    print('segment type     : %s' % ana.getDw())
    print('permission flag  : %s' % ana.getDw())
    print('offset           : %s' % ana.getQw())
    print('virutal addr     : %s' % ana.getQw())
    print('physical addr    : %s' % ana.getQw())
    print('filesize         : %s' % ana.getQw())
    print('memory size      : %s' % ana.getQw())
    print('align            : %s' % ana.getQw())


shoff = ana.getKeyEntry('sh-offset') 
shsize = ana.getKeyEntry('shsize')

print("\n ------------- string section ------------- \n")
strIndex = ana.getKeyEntry('str-section-index')
ana.setPos(shoff + (shsize * strIndex) + 24)

offset = ana.getQw()
size = ana.getQw()
sectionStr = ''.join(map(chr, ana.getRange(offset, size)))
for sect in sectionStr.split("\0"):
    print(sect)

print("\n ------------- section header ------------- \n")
ana.setPos(ana.getKeyEntry('sh-offset') + ana.getKeyEntry('shsize'))

for i in range(1, ana.getKeyEntry('shnum')):
    sni = ana.getDw() # section name index
    s = sectionStr[sni:]
    s = s[:s.find("\0", 1)]
    
    print(" ----- section header : %s ----- " % s)
    print('section name index   : %s' % sni)
    print('section type         : %s' % ana.getDw())
    print('section flag         : %s' % ana.getQw())
    print('address              : %s' % ana.getQw())
    print('offset               : %s' % ana.getQw())
    print('size                 : %s' % ana.getQw())
    print('link                 : %s' % ana.getDw())
    print('info                 : %s' % ana.getDw())
    print('address align        : %s' % ana.getQw())
    print('entry table size     : %s' % ana.getQw())
    print("")
