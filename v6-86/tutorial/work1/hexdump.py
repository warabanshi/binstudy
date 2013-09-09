from struct import unpack

f = open("a.out", "rb")
bindata = f.read()

hexdumpList = map(lambda x: hex(ord(x)), bindata)
print hexdumpList

tsize, dsize = unpack('<HH', bindata[2:6])
memdumpList = map(lambda x: hex(ord(x)), bindata[16:16+tsize+dsize])
print memdumpList
