# coding=utf-8
from subprocess import DEVNULL, PIPE, STDOUT, check_output, check_call, CalledProcessError
from utilities import mongolog, command_success, command_error
import os.path
import inspect
#import urllib.parse

from pwd import getpwuid, getpwnam
from grp import getgrgid


#Returns user cron as shown by command "crontab -l"
def getusercron(user):
    
    filename = '/var/spool/cron/crontabs/' + user

    with open(filename, 'w') as opened:
        opened

#    return command_success( getpwuid(os.stat('/var/spool/cron/crontabs/' + user).st_uid).pw_name )
    return command_success( getgrgid(os.stat('/var/spool/cron/crontabs/' + user).st_gid).gr_name )

    if not os.path.isfile('/var/spool/cron/crontabs/' + user):
        return command_success( 'No crontab found for user "' + user + '"' )

    command = ['crontab', '-l']

    try:
        output = check_output(command, stderr=PIPE, universal_newlines=True)
    except CalledProessError as e:
        return command_error(e, command)

    return command_success( output )


#def edituserrontab
