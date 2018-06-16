from utilities import filerename, filecopy, mongocheck, mongostart
import os

if os.path.isdir('/tmp/filesicuramenteinesistente'):
    print("a dir")
else:
    print("other")
