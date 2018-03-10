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

    #Gets enable vhosts
    enabled = set( os.listdir(apacheconfdir + 'sites-enabled') )
    #Gets nonactive vhosts
    notactive = set( os.listdir(apacheconfdir  + 'sites-available') ).difference(enabled)
    
    vhosts = list()

    for vhost in enabled:


        vhostspecs = { 'filename': vhost, 'active': 1 }

        with open(apacheconfdir + 'sites-enabled/' + vhost) as opened:
            vhostcontent = opened.read().splitlines()


        for line in vhostcontent:
            line = line.lstrip()
            linestosearch = ('DocumentRoot', 'ServerName', 'ServerAlias')
            print(line)

            if any( line.startswith(s) for s in linestosearch ):
                print('QUI' + line)
                vhostspecs.update({ line.split() })
        vhosts.append( vhostspecs )

#    for line in notactive: vhosts.append({ 'filename': line, 'active': 0 })

    return vhosts
