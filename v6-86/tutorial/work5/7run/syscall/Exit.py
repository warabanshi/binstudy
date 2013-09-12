import sys
from GlobalModel import GlobalModel as gm

class Exit(object):

    @staticmethod
    def execute():
        sys.exit(gm.getReg('ax'))
        

    @staticmethod
    def getArgc():
        return 0
