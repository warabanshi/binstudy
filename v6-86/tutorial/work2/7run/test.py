from struct import *
from nimonic.Mov import *
from Utils import *
from GlobalModel import GlobalModel as gm


#def testMov():
#    
#    binStr = pack('BBB', 0xb8, 0x00, 0x10)
#    Mov.execute(0, binStr, 0xb8)
#
#testMov()

def testGlobalModel():
    f = open('a.out', 'rb')
    header = f.read(16)
    tsize, dsize = unpack('<HH', header[2:6])
    
    text = f.read(tsize)

    print map(ord, text)
    print "tsize=%d, dsize=%d" % (tsize, dsize)
    gm.initData(len(text), text + f.read(dsize))

    print gm.getData(16, 11)
    print gm.setData(16, pack('<2B', 0x48, 0x45))
    print gm.getData(16, 11)


testGlobalModel()
