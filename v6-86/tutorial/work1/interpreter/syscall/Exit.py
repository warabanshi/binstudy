import sys
from Register import Register as reg

class Exit(object):

    @staticmethod
    def execute():
        sys.exit(reg.getReg('ax'))
        

    @staticmethod
    def getArgc():
        return 0
