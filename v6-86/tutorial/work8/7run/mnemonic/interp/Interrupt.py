from syscall.Write import Write as write
from syscall.Exit import Exit as exit
from GlobalModel import GlobalModel as gm
from Utils import *
from mnemonic.Mnemonic import Mnemonic

class Interrupt(Mnemonic):

    @staticmethod
    def execute(pc, text):
        mnemonic, val, inst = map(ord, text[0:3])
        pcInc = 3

        if val == 7:
            # system call
            None
        else:
            raise Exception("interrupt received unknown value: " + str(val))

        if inst == 0x04:
            # write
            offset, length = write.getArgv(text[pcInc:])
            write.execute(offset, length)
            pcInc += write.getArgc()

        elif inst == 0x01:
            # exit
            exit.execute()
            pcInc += exit.getArgc()

        else:
            raise Exception("unknown systemcall specified")

        return pcInc
