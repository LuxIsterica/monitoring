from pprint import pprint
from network import ifacestat
from logs import getlog
from apps import aptshow


pprint( aptshow('vim') )

exit()
pprint( getlog( dategte="2018-06-13", datelte="2018-06-14" )['data'] )
