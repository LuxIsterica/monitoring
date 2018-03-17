from user import getusers, getuser, getgroups, addusertogroups, removeuserfromgroups, adduser, removeuser, updateuserpass, updateusershell
from apps import listinstalled, aptsearch, aptshow, aptinstall, aptremove, aptupdate, addrepo,  getexternalrepos, removerepofile
from system import hostname, getsysteminfo
from systemfile import updatedb, locate, removefile
from apache import getvhosts, getmods, getconf, activatevhost, deactivatevhost
from pprint import pprint
from utilities import filedit
import os



repospath = '/etc/apt/sources.list.d/'
reposfiles = os.listdir(repospath)
print(reposfile)


#TODO: non cancellare le righe successive, discutere con Lucia dei Keyword Arguments
exit()
for i in listinstalled( summary=True ):
    print(i)

removeuser('temp', removehome=True)
