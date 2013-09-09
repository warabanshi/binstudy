from headers.Sh import Sh
from sections.SecDynamic   import SecDynamic
from sections.SecDynstr    import SecDynstr
from sections.SecDynsym    import SecDynsym
from sections.SecEhFrame   import SecEhFrame
from sections.SecGnuHash   import SecGnuHash
from sections.SecGnuVersion import SecGnuVersion
from sections.SecGnuVersionR import SecGnuVersionR
from sections.SecGotPlt    import SecGotPlt
from sections.SecHash      import SecHash
from sections.SecInterp    import SecInterp
from sections.SecPlt       import SecPlt
from sections.SecRelaPlt   import SecRelaPlt
from sections.SecShstrtab  import SecShstrtab
from sections.SecText      import SecText

class SectionManager(object):

    def __init__(self, text):
        self.sectionList = []

        secInterp       = SecInterp()
        secDynstr       = SecDynstr()
        secText         = SecText()

        secDynamic      = SecDynamic()
        secDynsym       = SecDynsym()
        secEhFrame      = SecEhFrame()
        secGnuHash      = SecGnuHash()
        secGnuVersion   = SecGnuVersion()
        secGnuVersionR  = SecGnuVersionR()
        secGotPlt       = SecGotPlt()
        secHash         = SecHash()
        secPlt          = SecPlt()
        secRelaPlt      = SecRelaPlt()
        secShstrtab     = SecShstrtab()

    def append(self, name, body, sh):
        self.sectionList.append({
            'name': name, 'body': body, 'sh': sh
        })

    def find(self, needle):
        for (idx, h) in enumerate(self.sectionList):
            if needle == h['name']:
                return idx

    def get(self, key = None):
        if key == None:
            return self.sectionList
       
        if isinstance(key, int):
            return self.sectionList[key]
        else:
            idx = self.find(key)

        if idx == None:
            return None
        else:
            return self.get(idx)


