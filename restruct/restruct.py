from elf.Utils import *
from elf.components.headers.Eh import Eh
from elf.components.headers.Sh import Sh
from elf.components.Section import Section
from elf.components.SectionAggregator import SectionAggregator

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

secAggr.dump()

# restruct phase
