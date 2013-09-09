from Utils import *
from struct import unpack

import sys

class Write(object):

    @staticmethod
    def execute(dataoffset, length, text):
        data = text[dataoffset:dataoffset+length]
        sys.stdout.write(data)

    @staticmethod
    def getArgv(text):
        return unpack('<HH', text[0:4])

    @staticmethod
    def getArgc():
        return 2
