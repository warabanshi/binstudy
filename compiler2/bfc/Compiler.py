import sys
import os.path
from Translator import Translator
from MakeElf import MakeElf

class Compiler:

    def __init__(self):
        try:
            inName = sys.argv[1]
        except:
            print 'error: must specify target filename'
            sys.exit(1)
          
        if not os.path.exists(inName):
            print 'file doesnt exists: ' + inName
            sys.exit(1)

        try:
            outName = sys.argv[2]
        except:
            outName = 'a.out'

        self.inName = inName
        self.outName = outName

    def execute(self):
        print('compile: ' + self.inName + ' to ' + self.outName)

        source = open(self.inName).read()
        t = Translator()
        t.translate(source)

        # for debug
        print t.getFuncList()
        print t.getAddrList()

        e = MakeElf(t)
        e.execute()

        f = open(self.outName, 'wb')
        #f.write(elf)
        f.write(text)
