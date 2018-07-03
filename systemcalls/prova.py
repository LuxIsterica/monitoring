from user import getusers, getuser, getgroups, getshells, updateusershell, getusernotgroups, getusergroups, addusertogroups, removeuserfromgroups, updateuserpass, adduser, removeuser
from apps import listinstalled, aptsearch, aptshow, getreponame, addrepo, removerepofile, getexternalrepos, aptupdate, aptremove, aptinstall
from apps import externalreposdir
from systemfile import locate,updatedb
from system import getsysteminfo, hostname
from network import ifacestat, getnewifacealiasname, createalias, destroyalias, ifaceup,ifacedown
from apache import apachestart, apachestop, apacherestart, apachereload, apachestatus, getvhosts, getmods, getconf, activatevhost, deactivatevhost, activatemod, deactivatemod, activateconf, deactivateconf
from apache import apacheconfdir
from cron import listcrontabs, addcron, addhourlycron, adddailycron, addweeklycron, addmonthlyycron, getcronname
from utilities import readfile, writefile, filedel, filecopy, filerename, mongocheck, mongostart, readdir
from logs import getlog
import os
import sys

'''als = list()
face = ifacestat()['data']
for key, value in face.items():
	als.append(getnewifacealiasname(key))
print(lista)'''
#print(destroyalias('enp0s3:0')['data'])
print(readdir("/home/lux/Scrivania")['data'])

#TODO: non cancellare le righe successive, discutere con Lucia dei Keyword Arguments
exit()
for i in listinstalled( summary=True ):
    print(i)

removeuser('temp', removehome=True)
