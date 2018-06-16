from utilities import filerename, filecopy
import os


result = filecopy('/root/test', '/root/nomodo/testa')
print( result['logid'] if result['returncode'] is 0 else result )
