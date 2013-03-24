from elf.Utils import *
from elf.Relation import *
from elf.components.headers.Eh import Eh
from elf.components.headers.Sh import Sh
from elf.components.Section import Section
from elf.components.SectionAggregator import SectionAggregator
from elf.components.SegmentMaker import SegmentMaker

import sys
from ctypes import *

# teardown ELF file
f = open('test.out')
byteList = map(lambda x: int(ord(x)), f.read())

# get ELF header
eh = Eh()
eh.retrieve(byteList[0:64])

shSize = eh.get('sh_size')
shNum = eh.get('sh_num')
shOff = eh.get('sh_offset')

# get sh string table
shStrStart = shOff + shSize * eh.get('shstrndx')

strSh = Sh()
strSh.retrieve(byteList[shStrStart:shStrStart+shSize])

strOff = strSh.get('offset')
strSize= strSh.get('size')
strTab = ''.join(map(chr, byteList[strOff:strOff+strSize]))

# get sections
secAggr = SectionAggregator()
for idx in range(1, shNum):

    if idx == eh.get('shstrndx'):
        continue

    shStart = shOff + shSize * idx

    sh = Sh()
    sh.retrieve(byteList[shStart:shStart+shSize])

    name = retrieveStr(strTab, sh.get('name_index'))
    body = byteList[sh.get('offset'):sh.get('offset')+sh.get('size')]

    secAggr.append(Section(body, name, sh))

# restruct phase
segMake = SegmentMaker(secAggr)
segMake.make()
segMake.setOffset()
segMake.setSize()
segMake.setAddr(0x400000)

# make shstrtbl
endOfBody = segMake.resetSection()

# remake ELF header
eh.set('entry_addr', segMake.getEntryAddr())
eh.set('ph_offset', 0x40)
eh.set('sh_offset', endOfBody)
eh.set('ph_num', segMake.getCount())
eh.set('sh_num', secAggr.count()+1)             # plus null section
eh.set('shstrndx', secAggr.find('.shstrtab')+1) # plus null section

# make output byte list
byteList = eh.output()

for key in orderList:
    seg = segMake.getSegment(key)
    if seg == None:
        continue

    byteList += seg.getPh().output()

for sec, name in segMake.getSectionList():
    body = sec.getBodyList()
    align = sec.getSh().get('address_align')
    mod = len(body) % align

    if mod > 0:
        body += [0x00 for i in range(align - mod)]

    byteList += body

byteList += [0x00 for i in range(64)]   # add null section header

for sec, name in segMake.getSectionList():
    byteList += sec.getSh().output()

# output to file
p = (c_ubyte * len(byteList))()
p[:] = byteList
with open('elf.out', 'wb') as fp:
    fp.write(p)
