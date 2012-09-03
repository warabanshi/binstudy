'''
JIT sample2

set to malloc will returns the value which type is Array.
if malloc returns POINTER then it doesn't recognize to sequence
thus they can't using the some instruction likely slice.

why malloc function returns "malloc(size)[0]" ?
it is dereference for the cause of getting the array from pointer.
if you setted to malloc.restype with ARRAY then return of malloc() is
array object which isn't pointer of array.
'''
from ctypes import *

libc = cdll.LoadLibrary("libc.so.6")
free = libc.free
printf = libc.printf

def malloc(size):
    malloc = libc.malloc
    malloc.restype = POINTER(ARRAY(c_ubyte, size))
    return malloc(size)[0]

p = malloc(4)
p[:] = [ord('d'), ord('e'), ord('f'), 0]
printf(p)

free(p)
