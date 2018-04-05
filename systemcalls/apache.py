# coding=utf-8
from subprocess import Popen, DEVNULL, PIPE, STDOUT, check_output, check_call, CalledProcessError
from utilities import mongolog, command_success, command_error
import os
import re
import datetime
import pprint
import inspect
#import urllib.parse


#NOTE: Never call this function directly.
#objtype can be one of "sites", "mods" or "conf"
def getobjs(objtype):

    apacheconfdir = "/etc/apache2/"
    availabledir = objtype + '-available/'
    enableddir = objtype + '-enabled/'

    objs = list()

    #Getting enabled vhosts and appending to vhosts list as dictionary
    enabled = set( os.listdir(apacheconfdir + enableddir ) )
    for obj in enabled:
        objs.append({ 'filename': obj, 'active': 1 })

    #Gets nonactive vhosts and appending to vhosts list as dictionary
    notactive = set( os.listdir(apacheconfdir  + availabledir) ).difference(enabled)
    for obj in notactive:
        objs.append({ 'filename': obj, 'active': 0 })



    ##### ONLY FOR VHOSTS #####
    #Gathering object information only if objstype == "site"
    if objtype is "sites":
        #Gathering vhosts information to fill the list
        for obj in objs:

            #"vhostcontent" mantains all vhost file content
            with open(apacheconfdir + availabledir + obj['filename']) as opened:
                vhostcontent = opened.read().splitlines()

            
            i = 0
            for line in vhostcontent:
                line = line.lstrip()
                linestosearch = ('Alias', 'DocumentRoot', 'ServerName', 'ServerAlias')

                #If any of this words in vhost file add the entire splitted line to the vhost dict
                if any( line.startswith(s) for s in linestosearch ):

                    #A vhost can handle multiple ServerAlias but dict() cannot accept multiple key with the same string
                    #so we're going to add an incremental number to the key "ServerAlias"
                    if 'ServerAlias' in  line: line = re.sub('ServerAlias', 'ServerAlias' + str(i), line)
                    i += 1

                    line = line.split(None, maxsplit=1)

                    #vhost dict is a pointer to the original dict in vhosts list, hence an update here means an update to the original dict
                    obj.update({ line[0]: line[1] })


    return command_success(objs)

def getvhosts(): return getobjs('sites')
def getmods(): return getobjs('mods')
def getconf(): return getobjs('conf')



#NOTE: Must not be called directly
def manageapache(op):
    
    #Can only accept these parameters
    acceptedparams = ['stop', 'status', 'reload', 'restart']
    if not any(op in param for param in acceptedparams):
        return dict({
            'returncode': -1,
            ('message', 'stderr'): 'Bad parameter :' + op
        })
    else:
        command = ['systemctl', op, 'apache2']


    toreturn = None
    try:
        if op is "status":
            #Avoid to print journal (log) lines in output
            command.append('-n0')

            #We are using Popen here because check_output fails to return stdout and stderr on exit code != 0
            toreturn = Popen(command, stdout=PIPE, universal_newlines=True).communicate()[0].splitlines()

            #Filtering useless lines
            linestomantain = ['active', 'memory', 'cpu']
            toreturn = list( filter( lambda line: any(s in line.lower() for s in linestomantain), toreturn ) )
            #Formatting output
            toreturn = dict( map(lambda line: line.lstrip().split(':', maxsplit=1), toreturn ) )

        else:
            #Logging operation to MongoDB; in this specific case "toreturn" contains mongo logid
            toreturn = mongolog( locals() )
            check_call(command)
    except CalledProcessError:
        pass


    return command_success(toreturn)

def apachestart(): return manageapache(op='start')
def apachestop(): return manageapache(op='stop')
def apacherestart(): return manageapache(op='restart')
def apachereload(): return manageapache(op='reload')
def apachestatus(): return manageapache(op="status")




#NOTE: Must not be called directly
def manageobjs(filename, op):
    logid = mongolog( locals() )

    command = [op, filename]

    try:
        #Shrinks the output --------.
        #                           |
        #                           v
        check_call(command, stdout=DEVNULL)
    except CalledProcessError as e:
        return command_error(e, command)

    #Reloading apache after site activation
    apachereload()

    return command_success(logid)

#Call a function with different parameters
def activatevhost(filename): return manageobjs(filename, op='a2ensite')
def deactivatevhost(filename): return manageobjs(filename, op='a2dissite')
def activatemod(filename): return manageobjs(filename, op='a2enmod')
def deactivatemod(filename): return manageobjs(filename, op='a2dismod')
def activateconf(filename): return manageobjs(filename, op='a2enconf')
def deactivateconf(filename): return manageobjs(filename, op='a2disconf')
