def convNum(byteList, byteNum):
    if len(byteList) < byteNum:
        return 0

    result = 0
    for i in range(byteNum):
        result = (result << 8) | ord(byteList[i])

    return result

def convBytes(num, length):
    r = []
    for i in range(length):
        r.append(num & 0xff)
        num = num >> 8

    return r

def printInst(pc, nimonic, operand):
    print "%04x: %-13x %s" % (pc, nimonic, operand)
