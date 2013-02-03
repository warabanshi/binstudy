from elf.Analyze import Analyze
from elf.WriteElf import WriteElf

obj = Analyze('test.out')
w = WriteElf()

w.setEh(obj.getEh())
w.make()
