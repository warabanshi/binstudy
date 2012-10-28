import sys
from BfCompiler.NativeBf import *

f = open(sys.argv[1])
source = f.read()
f.close()

nbf = NativeBf(source)
bfbin = nbf.execute()
