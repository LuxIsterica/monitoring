from user import getusers, getuser, getgroups, getusergroups, getusernotgroups, addusertogroups, removeuserfromgroups, adduser, removeuser, updateuserpass, getshells, updateusershell
from apps import listinstalled, aptsearch, aptshow, aptinstall, aptremove, aptupdate, addrepo,  getexternalrepos, removerepofile
from system import hostname, getsysteminfo
from systemfile import updatedb, locate, removefile
from apache import getvhosts, getmods, getconf, activatevhost, deactivatevhost, apachestatus, apachereload
from pprint import pprint
from utilities import filediff, filedit
from network import ifacestat, getnewifacealiasname, ifacedown, ifaceup, editiface, createalias, destroyalias, getroutes, addroute, defaultroute, delroute
from cron import getusercron, writeusercrontab
import os
import sys



print('USERGROUP\n', getusergroups('giuseppe')['data'] )
print('GROUPS\n', getgroups(namesonly=True)['data'] )
print('USERNOTGROUP\n', getusernotgroups('giuseppe')['data'] )

<<<<<<< Updated upstream
<<<<<<< Updated upstream
data = writeusercrontab('giuseppe', 'nuovociaone')
=======
data = getvhosts()
#data = getusercron('giuseppe')
>>>>>>> Stashed changes
=======
exit()


data = getgroups(namesonly=True)
#data = writeusercrontab('giuseppe', 'nuovociaone')
>>>>>>> Stashed changes
if data['returncode'] is 0:
    data = data['data']

pprint(data)

#delroute( data )


#TODO: non cancellare le righe successive, discutere con Lucia dei Keyword Arguments
exit()
for i in listinstalled( summary=True ):
    print(i)

removeuser('temp', removehome=True)
