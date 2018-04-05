from user import getusers, getuser, getgroups, addusertogroups, removeuserfromgroups, adduser, removeuser, updateuserpass, getshells, updateusershell
from apps import listinstalled, aptsearch, aptshow, aptinstall, aptremove, aptupdate, addrepo,  getexternalrepos, removerepofile
from system import hostname, getsysteminfo
from systemfile import updatedb, locate, removefile
from apache import getvhosts, getmods, getconf, activatevhost, deactivatevhost, apachestatus, apachereload
from pprint import pprint
from utilities import filediff, filedit
from network import ifacestat, getnewifacealiasname, ifacedown, ifaceup, createalias, destroyalias
import os
import sys



data = destroyalias( 'eth0:1' )
data = createalias( getnewifacealiasname('eth0')['data'], address='10.100.10.192', netmask='255.255.0.0' )
if data['returncode'] is 0:
    data = data['data']

pprint(data)


#TODO: non cancellare le righe successive, discutere con Lucia dei Keyword Arguments
exit()
for i in listinstalled( summary=True ):
    print(i)

removeuser('temp', removehome=True)
