from pprint import pprint
from apps import aptupdate, aptremove

pprint( aptremove('sl', purge=True) )
