from syscall.Write import Write as write
from syscall.Exit import Exit as exit

class Interrupt(object):

    @staticmethod
    def execute(pc, text):
        nimonic, val, inst = map(ord, text[0:3])
        pcInc = 2

        if val == 7:
            # system call
            None
        else:
            raise Exception("interrupt received unknown value: " + str(val))
        pcInc += 1

        if inst == 0x04:
            # write
            offset, length = write.getArgv(text[pcInc:])
            write.execute(offset - pc, length, text)
            pcInc += write.getArgc()

        elif inst == 0x01:
            # exit
            exit.execute()
            pcInc += exit.getArgc()

        else:
            raise Exception("unknown systemcall specified")

        return pcInc
