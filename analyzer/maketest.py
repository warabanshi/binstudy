from elf.WriteElf import WriteElf
from elf.ReadElf import ReadElf

re = ReadElf('test.out')

phCtrl = re.getPhCtrl()
shCtrl = re.getShCtrl()

we = WriteElf(phCtrl, shCtrl)
we.make()
