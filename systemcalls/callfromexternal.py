from user import getusers, getuser, getgroups, addusertogroups, removeuserfromgroups, adduser, removeuser, updateuserpass, updateusershell
from apps import listinstalled, aptsearch, aptshow, aptinstall, aptremove, aptupdate, addrepo,  getexternalrepos, removerepofile
from system import hostname, etchosts, getsysteminfo
from systemfile import updatedb, locate, getsetfile, removefile
from apache import getvhosts, apache2, activatevhost, deactivatevhost
from pprint import pprint
import os




pprint( activatevhost('default-ssl') ) #test

#TODO: non cancellare le righe successive, discutere con Lucia dei Keyword Arguments
exit()
for i in listinstalled( summary=True ):
    print(i)

removeuser('temp', removehome=True)
