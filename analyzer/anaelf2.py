import sys, struct
from elf.Analyze import Analyze

obj = Analyze(sys.argv[1])

#obj.getEh().echo()
#obj.getPh(0).echo()
#obj.getSh(14).echo()
#print(map(hex, obj.getRange(0xe98, 0x200)))
#obj.getSh(14).echo()
#print(map(hex, obj.getRange(3736, 336)))
#print(map(chr, obj.getSh(6).getBody()))
#print(map(hex, obj.getSh(5).getBody()))
obj.echoSn()
print(map(chr, obj.getSh('.shstrtab').getBody()))
