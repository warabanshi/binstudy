'''
JIT sample1

write the values to memory by using C library

@see also http://python.net/crew/theller/ctypes/tutorial.html
'''

from ctypes import *

# load C library
libc = cdll.LoadLibrary("libc.so.6")

# make function synonim
malloc = libc.malloc
free = libc.free
printf = libc.printf

# set response type of malloc
malloc.restype = POINTER(c_ubyte)

p = malloc(4)
p[0] = ord('a')
p[1] = ord('b')
p[2] = ord('c')
p[3] = ord("\n")

printf(p)
free(p)
