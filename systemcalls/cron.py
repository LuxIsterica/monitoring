# coding=utf-8
from subprocess import DEVNULL, PIPE, STDOUT, check_output, check_call, CalledProcessError
from utilities import mongolog, command_success, command_error, writefile
from user import getuser
import os
import inspect
import datetime
#import urllib.parse


def listcrontabs():

    basedir = '/etc/'
    paths = ['cron.d', 'cron.daily', 'cron.hourly', 'cron.monthly', 'cron.weekly']

    cronlist = dict()
    for path in paths:
        flist = os.listdir(basedir + path)
        flist.remove('.placeholder') 
        cronlist.update({ path: flist })

    return command_success( data=cronlist )



def getcronname(): return 'nomodo-' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')


# New cron line gets executed every minute by default
def addcron( command, name="", user="root", minute='*', hour='*', dom='*', month='*', dow='*' ):

    cronspath = '/etc/cron.d/' 

    #New cron gets a random name if user did not provide it
    if not name: name = getcronname()

    logid = mongolog( locals() )

    with open(cronspath + name, 'w') as newcron:
        newcron.write( minute + ' ' + hour + ' ' + dom + ' ' + month + ' ' + dow + ' ' + user + ' ' + command + '\n' )

    return command_success( data=cronspath+name, logid=logid )


#in such a case "command" must be a bash script
def adddefaultcron(command, cronspath, name):

    #New cron gets a random name if user did not provide it
    if not name: name=getcronname()

    logid = mongolog( locals() )

    with open(cronspath + name, 'w') as newcron:
        newcron.write( command + '\n' )

    return command_success( data=cronspath+name, logid=logid )


def addhourlycron(command, name=""): return addefaultcron( name=name, command=command, cronspath='/etc/cron.hourly/' )
def adddailycron(command, name=""): return addefaultcron( command=command, cronspath='/etc/cron.daily/' )
def addweeklycron(command, name=""): return addefaultcron( command=command, cronspath='/etc/cron.weekly/' )
def addmonthlyycron(command, name=""): return addefaultcron( command=command, cronspath='/etc/cron.monthly/' )
