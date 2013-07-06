import sys
import os.path
from Translator import Translator

class Compiler:

    def __init__(self):
        try:
            inName = sys.argv[1]
        except:
            print 'error: must specify target filename'
            sys.exit(1)
          
        try:
            outName = sys.argv[2]
        except:
            outName = 'a.out'

        self.inName = inName
        self.outName = outName

    def execute(self):
        print('compile: ' + self.inName + ' to ' + self.outName)

        try:
            os.path.exists(self.inName)
        except:
            print 'file doesnt exists: ' + self.inName
            sys.exit(1)

        source = open(self.inName).read()
        t = Translator()
        text = t.translate(source)

        # for debug
        print t.getFuncList()
        print t.getAddrList()

        '''
        e = MakeElf()
        e.setText(text)
        e.linking()
        '''

        f = open(self.outName, 'wb')
        #f.write(elf)
        f.write(text)
