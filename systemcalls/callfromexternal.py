from user import getusers, getuser, getgroups, getusergroups, getusernotgroups, addusertogroups, removeuserfromgroups, adduser, removeuser, updateuserpass, getshells, updateusershell
from apps import listinstalled, aptsearch, aptshow, aptinstall, aptremove, aptupdate, addrepo,  getexternalrepos, removerepofile
from system import hostname, getsysteminfo
from systemfile import updatedb, locate, removefile
from apache import getvhosts, getmods, getconf, activatevhost, deactivatevhost, apachestatus, apachereload
from pprint import pprint
from utilities import filediff, writefile
from network import ifacestat, getnewifacealiasname, ifacedown, ifaceup, editiface, createalias, destroyalias, getroutes, addroute, defaultroute, delroute
from cron import listcrontabs, getcroncontent, addcron, addhourlycron, writecron
import os
import sys



data = addcron( command="echo nomodotest >> /tmp/nomodocron" )
print( data['data'] if data['returncode'] is 0 else data['stderr'] )

exit()
data = addhourlycron(command='#!/bin/bash\necho "nomodocron" >> /tmp/nomodocron')
print( data['logid'] if data['returncode'] is 0 else data['stderr'] )
