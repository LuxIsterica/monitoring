from user import getusers, getuser, getgroups, getusergroups, getusernotgroups, addusertogroups, removeuserfromgroups, adduser, removeuser, updateuserpass, getshells, updateusershell
from apps import listinstalled, aptsearch, aptshow, aptinstall, aptremove, aptupdate, addrepo,  getexternalrepos, removerepofile
from system import hostname, getsysteminfo
from systemfile import updatedb, locate, removefile
from apache import getvhosts, getmods, getconf, activatevhost, deactivatevhost, apachestatus, apachereload
from pprint import pprint
from utilities import filediff, filedit, mongostatuserror
from network import ifacestat, getnewifacealiasname, ifacedown, ifaceup, editiface, createalias, destroyalias, getroutes, addroute, defaultroute, delroute
from cron import getusercron, writeusercrontab
from bson.objectid import ObjectId
import os
import sys



logid = adduser('giuseppe2', 'test')['data']
print( logid.toString() )
#print( mongostatuserror(logid) )



exit()
data = getsysteminfo()
if data['returncode'] is 0:
    (cpu, mem, proc) = data['data']

pprint(proc)


#TODO: non cancellare le righe successive, discutere con Lucia dei Keyword Arguments
exit()
for i in listinstalled( summary=True ):
    print(i)

removeuser('temp', removehome=True)
