from user import getusers, getuser, getgroups, getusergroups, getusernotgroups, addusertogroups, removeuserfromgroups, adduser, removeuser, updateuserpass, getshells, updateusershell
from apps import listinstalled, aptsearch, aptshow, aptinstall, aptremove, aptupdate, addrepo,  getexternalrepos, removerepofile
from system import hostname, getsysteminfo
from systemfile import updatedb, locate
from apache import getvhosts, getmods, getconf, activatevhost, deactivatevhost, apachestatus, apachereload, apacheconfdir
from pprint import pprint
from utilities import filediff, writefile, readfile, filedel, mongocheck
from network import ifacestat, getnewifacealiasname, ifacedown, ifaceup, editiface, createalias, destroyalias, getroutes, addroute, defaultroute, delroute
from cron import listcrontabs, addcron, addhourlycron
import os
import sys

als = list()
face = ifacestat()['data']
for key, value in face.items():
	als.append(getnewifacealiasname(key))
print(lista)

#TODO: non cancellare le righe successive, discutere con Lucia dei Keyword Arguments
exit()
for i in listinstalled( summary=True ):
    print(i)

removeuser('temp', removehome=True)
