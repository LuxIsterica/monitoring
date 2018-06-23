from pprint import pprint
from logs import getlog
from apps import aptshow


pprint( aptshow('nginx')['data'] )

exit()
pprint( getlog( dategte="2018-06-13", datelte="2018-06-14" )['data'] )
