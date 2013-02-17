from elf.components.headers.Sh import Sh
from elf.components.SectionController import SectionController
from elf.components.SegmentController import SegmentController
from elf.components.Section import Section
from elf.WriteElf import WriteElf
from elf.Utils import *

sctCtrl = SectionController()

#.text header
name = '.text'
byteList =  [0xb8, 0x3c, 0x00, 0x00, 0x00]
byteList += [0xbf, 0x2a, 0x00, 0x00, 0x00]
byteList += [0x0f, 0x05]
sh = Sh()
sh.set('type', 3)
sh.set('flag', 6)
sh.set('size', len(byteList))
sh.set('address_align', 1)
sh.set('entry_table_size', 0)

sctCtrl.append(Section(byteList, name, sh))

# dummy for test
name = '.interp'
byteList =  [0xb8, 0x3c, 0x00, 0x00, 0x00]
byteList += [0xbf, 0x2a, 0x00, 0x00, 0x00]
byteList += [0x0f, 0x05]
sh = Sh()
sh.set('type', 3)
sh.set('flag', 6)
sh.set('size', len(byteList))
sh.set('address_align', 1)
sh.set('entry_table_size', 0)

sctCtrl.append(Section(byteList, name, sh))
sctNull, sctList, sctStr = sctCtrl.getSectionList()

segCtrl = SegmentController()
sctList = segCtrl.makeSegment(sctList)


#we = WriteElf(sCtrl)
#we.make()
