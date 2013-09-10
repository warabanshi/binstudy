from syscall.Write import Write as write
from syscall.Exit import Exit as exit
from GlobalModel import GlobalModel as gm
from Utils import *

class Interrupt(object):

    @staticmethod
    def execute(pc, text):
        nimonic, val, inst = map(ord, text[0:3])

        if gm.isReverse():
            printInst(pc, convNum(text, 2), 'int ' + str(val))
            pcInc = 2
        else:
            pcInc = 3

        if val == 7:
            # system call
            None
        else:
            raise Exception("interrupt received unknown value: " + str(val))

        if inst == 0x04:
            # write
            if gm.isReverse():
                pcInc += Interrupt.printReverse(pc+pcInc, write.getArgc(), text[pcInc:], 'write')
            else:
                offset, length = write.getArgv(text[pcInc:])
                write.execute(offset, length)
                pcInc += write.getArgc()

        elif inst == 0x01:
            # exit
            if gm.isReverse():
                pcInc += Interrupt.printReverse(pc+pcInc, exit.getArgc(), text[pcInc:], 'exit')
            else:
                exit.execute()
                pcInc += exit.getArgc()

        else:
            raise Exception("unknown systemcall specified")

        return pcInc

    @staticmethod
    def printReverse(pc, argc, text, instName):
        printInst(pc, convNum(text, 1), '; sys ' + instName)
        pcInc = 1

        for i in range(argc):
            printInst(pc+pcInc, convNum(text[pcInc:], 2), '; arg')
            pcInc += 2

        return pcInc

