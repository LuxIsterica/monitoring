from user import getusers, getuser, getgroups, getusergroups, getusernotgroups, addusertogroups, removeuserfromgroups, adduser, removeuser, updateuserpass, getshells, updateusershell
from apps import listinstalled, aptsearch, aptshow, aptinstall, aptremove, aptupdate, addrepo,  getexternalrepos, removerepofile
from system import hostname, getsysteminfo
from systemfile import updatedb, locate
from apache import getvhosts, getmods, getconf, activatevhost, deactivatevhost, apachestatus, apachereload, apacheconfdir
from pprint import pprint
from utilities import filediff, writefile, readfile, delfile
from network import ifacestat, getnewifacealiasname, ifacedown, ifaceup, editiface, createalias, destroyalias, getroutes, addroute, defaultroute, delroute
from cron import listcrontabs, getcroncontent, addcron, addhourlycron, writecron
import os
import sys



data = getsysteminfo()
#data = writeusercrontab('giuseppe', 'nuovociaone')
(cpu,mem,proc) = data['data']
if data['returncode'] is 0:
    #(cpu,mem,proc) = data['data']
	#pprint(data['data'][1]['filename'][:-5])
	print (data)


#TODO: non cancellare le righe successive, discutere con Lucia dei Keyword Arguments
exit()
for i in listinstalled( summary=True ):
    print(i)

removeuser('temp', removehome=True)
