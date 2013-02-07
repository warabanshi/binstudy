from elf.WriteElf import WriteElf
from elf.ReadElf import ReadElf

re = ReadElf('test.out')
eh, phCtrl, shCtrl = re.getResult()


#we = WriteElf(phCtrl, shCtrl)
#we.make()
