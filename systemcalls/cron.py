# coding=utf-8
from subprocess import DEVNULL, PIPE, STDOUT, check_output, check_call, CalledProcessError
from utilities import mongolog, command_success, command_error, filedit
import os.path
import inspect
#import urllib.parse

from pwd import getpwuid, getpwnam
from grp import getgrgid


#Returns user cron as shown by command "crontab -l"
def getusercron(user):
    
    crontab = '/var/spool/cron/crontabs/' + user

    #On file 
    if not os.path.isfile( crontab ):
        return command_success( 'No crontab found for user "' + user + '"' )

    command = ['crontab', '-l']

    try:
        output = check_output(command, stderr=PIPE, universal_newlines=True)
    except CalledProessError as e:
        return command_error(e, command, logid)

    return command_success( output )


def writeusercrontab(user, newcron):
    
    userscronpath = '/var/spool/cron/crontabs/'

    return filedit( userscronpath + user, newcron )
