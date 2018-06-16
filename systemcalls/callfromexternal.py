from utilities import filerename, filecopy, mongocheck, mongostart
import os


result = mongostart()
print( 'ok' if result['returncode'] is 0 else result )
