import sys, struct
from elf.Analyze import Analyze

obj = Analyze(sys.argv[1])

#obj.getEh().echo()
#obj.getPh(0).echo()
obj.getSh(14).echo()
