from struct import unpack

def convNum(byteList, byteNum):
    if len(byteList) < byteNum:
        return 0

    result = 0
    for i in range(byteNum):
        result = (result << 8) | byteList[i]

    return result

def printLn(pc, nimonic, operand):
    print "%04x: %-13x %s" % (pc, nimonic, operand)

def printMov(pc, txt):
    nimonic, val, register = txt[0:3]
    if register == 0x00:
        regName = 'ax'
    else:
        regName = 'unknown'

    inst = 'mov %s, %04x' % (regName, val)
    printLn(pc, convNum(txt, 3), inst)

def printInt(pc, txt):
    nimonic, val, inst = txt[0:3]
    printLn(pc, convNum(txt, 2), 'int ' + str(val))
    pcInc = 2

    if inst == 0x4:
        argc = 2
        instName = 'write'
    elif inst == 0x1:
        argc = 0
        instName = 'exit'
    else:
        argc = 0
        instName = 'unknown'

    printLn(pc+pcInc, convNum(txt[pcInc:], 1), '; sys ' + instName)
    pcInc += 1

    for i in range(argc):
        printLn(pc+pcInc, convNum(txt[pcInc:], 2), '; arg')
        pcInc += 2

    return pcInc

f = open("a.out", "rb")
header = f.read(16)
tsize, dsize = unpack('<HH', header[2:6])

memdata = map(lambda x: ord(x), f.read(tsize+dsize))
#print map(hex, memdata)

pc = 0
while pc < len(memdata):
    txt = memdata[pc:]

    if convNum(txt, 1) == 0xb8:
        printMov(pc, txt)
        pc += 3

    elif convNum(txt, 1) == 0xcd:
        pc += printInt(pc, txt)
    else:
        pc += 1
