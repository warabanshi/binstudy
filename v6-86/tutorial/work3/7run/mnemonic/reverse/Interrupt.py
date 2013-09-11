from syscall.Write import Write as write
from syscall.Exit import Exit as exit
from GlobalModel import GlobalModel as gm
from Utils import *
from mnemonic.Mnemonic import Mnemonic

class Interrupt(Mnemonic):

    @staticmethod
    def execute(pc, text):
        mnemonic, val, inst = map(ord, text[0:3])

        printInst(pc, convNum(text, 2), 'int ' + str(val))
        pcInc = 2

        if val == 7:
            # system call
            None
        else:
            raise Exception("interrupt received unknown value: " + str(val))

        if inst == 0x04:
            # write
            pcInc += Interrupt.printReverse(
                pc+pcInc, write.getArgc(), text[pcInc:], 'write'
            )

        elif inst == 0x01:
            # exit
            pcInc += Interrupt.printReverse(
                pc+pcInc, exit.getArgc(), text[pcInc:], 'exit'
            )

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

