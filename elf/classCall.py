import sys
from BfCompiler.NativeBf import *

f = open(sys.argv[1])
source = f.read()
f.close()

nbf = NativeBf(source)
if (len(sys.argv) > 1):
    nbf.execute(sys.argv[2])
else:
    nbf.execute()
