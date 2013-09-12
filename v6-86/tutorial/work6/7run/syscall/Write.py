from Utils import *
from struct import unpack
from GlobalModel import GlobalModel as gm

import sys

class Write(object):

    @staticmethod
    def execute(offset, length):
        data = gm.getData(offset, length)
        sys.stdout.write(data)

    @staticmethod
    def getArgv(text):
        return unpack('<HH', text[0:4])

    @staticmethod
    def getArgc():
        return 2
