from utilities import filerename


lista = list()
if not lista:
    print('lista vuota')
else:
    print('ci sta qualcosa')

exit()
result = filerename('/root/test', 'testa' )
print( result['logid'] if result['returncode'] is 0 else result )
