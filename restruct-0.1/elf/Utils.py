# convert val of specified number of byte to
# little endian list inlucdes each byte
def convLE(val, byteNum):
    le = []
    for i in range(byteNum):
        le.append((val >> i*8) & 0xff)

    return le

# convert from list to little endian binary value
# regards list elements are single byte respectively
def convBin(li):
    b = 0
    for byte in reversed(li):
        b = (b << 8) | byte

    return b

def retrieveStr(shStr, index):
    s = shStr[index:]
    return s[:s.find("\0")]

