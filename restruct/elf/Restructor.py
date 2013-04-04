from elf.Utils import *
from elf.Relation import *
from elf.components.SectionExtractor import SectionExtractor
from elf.components.SectionManager import SectionManager
from elf.components.SegmentManager import SegmentManager
from elf.components.headers.Eh import Eh

import sys
from ctypes import *

class Restructor(object):

    def __init__(self, fn):
        f = open(fn)
        self.byteList = map(lambda x: int(ord(x)), f.read())
        f.close()

    def restruct(self):
        secm = SectionManager()
        segm = SegmentManager()
        se = SectionExtractor(self.byteList)

        for name, body, sh in se.extract():
            secm.append(name, body, sh)
        
        segm.mapping(secm)

        headerSize = 0x40 + len(segm.getSegmentList()) * 56
        body = secm.makeBody(headerSize)
        phList = segm.makePh(secm)
        secm.resetAddress(0x400000)
        print(hex(len(body)+headerSize))
        shStrTab = secm.makeShStrSection(headerSize + len(body))

        endOfBody = headerSize + len(body + shStrTab)

        eh = Eh()
        eh.retrieve(self.byteList[0:64])
        eh.set('entry_addr', secm.get('.text')['sh'].get('address'))
        eh.set('ph_offset', 0x40)
        eh.set('sh_offset', endOfBody)
        eh.set('ph_num', len(phList))
        eh.set('sh_num', len(secm.get())+1) # plus null section
        eh.set('shstrndx', secm.find('.shstrtab')+1)

        #eh.echo()

        byteList = eh.output()
        for ph in phList:
            byteList += ph.output()

        byteList += body
        byteList += shStrTab

        byteList += [0x00 for x in range(64)]
        for h in secm.get():
            byteList += h['sh'].output()

        p = (c_ubyte * len(byteList))()
        p[:] = byteList
        with open('elf.out', 'wb') as fp:
            fp.write(p)
