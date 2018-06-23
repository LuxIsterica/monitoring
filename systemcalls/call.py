from pprint import pprint
from logs import getlog
from apps import aptshow
from utilities import mongocheck

print( mongocheck()['returncode'] )

exit()
pprint( aptshow('vim') )

exit()
pprint( getlog( dategte="2018-06-13", datelte="2018-06-14" )['data'] )
