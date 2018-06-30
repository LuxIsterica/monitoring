from pprint import pprint
from utilities import readdir
from apps import aptshow

pprint( aptshow('curl') )


exit()
dircontent = readdir( '/etc/apache' )
pprint( dircontent['data'] if dircontent['returncode'] is 0 else dircontent['stderr'] )
