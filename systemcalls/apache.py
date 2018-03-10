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

    #Gets enable vhosts
    enabled = set( os.listdir('/etc/apache2/sites-enabled') )
    #Gets nonactive vhosts
    notactive = set( os.listdir("/etc/apache2/sites-available") ).difference(enabled)
    
    vhosts = list()

    for line in enabled: vhosts.append({ 'filename': line, 'active': 1 })
    for line in notactive: vhosts.append({ 'filename': line, 'active': 0 })

    return vhosts
