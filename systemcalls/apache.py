# coding=utf-8
from subprocess import Popen, PIPE, STDOUT, check_output, check_call, CalledProcessError
from utilities import mongolog, command_error
import os
import re
import datetime
import pprint
import inspect
#import urllib.parse

def getvhosts():

    apacheconfdir = "/etc/apache2/"
    availabledir = 'sites-available/'
    #There no need for 'sites-enabled' because we can find those vhosts in sites-available too

    vhosts = list()

    #Getting enable vhosts and appending to vhosts list as dictionary
    enabled = set( os.listdir(apacheconfdir + 'sites-enabled') )
    for vhost in enabled:
        vhosts.append({ 'filename': vhost, 'active': 1 })

    #Gets nonactive vhosts and appending to vhosts list as dictionary
    notactive = set( os.listdir(apacheconfdir  + 'sites-available') ).difference(enabled)
    for vhost in notactive:
        vhosts.append({ 'filename': vhost, 'active': 0 })


    
    #Filling the list to return with all information about every single vhost
    for vhost in vhosts:

        #"vhostcontent" mantains all vhost file content
        with open(apacheconfdir + availabledir + vhost['filename']) as opened:
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
                vhost.update({ line[0]: line[1] })


    return vhosts





def apache2(op="status"):
    
    #Can only accept these parameters
    acceptedparams = ['stop', 'status', 'reload', 'restart']
    if not any(op in param for param in acceptedparams):
        return {'errcode': -1, 'errmessage': 'Bad parameter :' + op}
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


    return toreturn



#NOTE: Must not be called directly
def managevhosts(filename, op):
    logid = mongolog( locals() )

    command = [op, filename]

    try:
        check_output = check_call(command)
    except CalledProcessError as e:
        return command_error(e, command)

    return logid
    apache2(op='reload')
    #Reloading apache after site activation

#Call a function with different parameters
def activatevhost(filename): managevhosts(filename, op='a2ensite')
def deactivatevhost(filename): managevhosts(filename, op='a2dissite')
