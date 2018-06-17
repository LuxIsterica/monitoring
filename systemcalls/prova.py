from user import getusers, getuser, getgroups, getusergroups, getusernotgroups, addusertogroups, removeuserfromgroups, adduser, removeuser, updateuserpass, getshells, updateusershell
from apps import listinstalled, aptsearch, aptshow, aptinstall, aptremove, aptupdate, addrepo,  getexternalrepos, removerepofile
from system import hostname, getsysteminfo
from systemfile import updatedb, locate
from apache import getvhosts, getmods, getconf, activatevhost, deactivatevhost, apachestatus, apachereload, apacheconfdir
from pprint import pprint
from utilities import filediff, writefile, readfile, filedel
from network import ifacestat, getnewifacealiasname, ifacedown, ifaceup, editiface, createalias, destroyalias, getroutes, addroute, defaultroute, delroute
from cron import listcrontabs, addcron, addhourlycron
import os
import sys

facestat = ifacestat()['data']
key_remove = []
als = []
for key,value in facestat.items():
	if 'LOOPBACK' in value[-1]:
		lo = facestat[key].copy()
		key_remove.append(key)
	elif ':' in key:
		als.append(facestat[key])
		key_remove.append(key)
for key in key_remove:
	del facestat[key]

if len(als) > 0:
	for a in als:
		print(a)	

print(facestat)

#TODO: non cancellare le righe successive, discutere con Lucia dei Keyword Arguments
exit()
for i in listinstalled( summary=True ):
    print(i)

removeuser('temp', removehome=True)
