from pprint import pprint
from  utilities import readdir

dircontent = readdir( '/etc/apache' )
pprint( dircontent['data'] if dircontent['returncode'] is 0 else dircontent['stderr'] )
