from pprint import pprint
from apps import aptupdate, aptremove, listinstalled

pprint( listinstalled()['data'] )

exit()
pprint( aptremove('sl', purge=True) )
