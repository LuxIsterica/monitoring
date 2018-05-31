# coding=utf-8
from subprocess import DEVNULL, PIPE, STDOUT, check_output, check_call, CalledProcessError
from utilities import mongolog, command_success, command_error, filedit
from user import getuser
import os
import inspect
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



def getcrontabcontent(path):

    try:
        with open(path, 'r') as content:
            return command_success( data=content.read() )
    except FileNotFoundError:
        return command_error( returncode=10, stderr='No cron file found: "'+path+'"' )


def editcrontab(path):
    pass

def newcrontab():
    pass




















##Returns user cron as shown by command "crontab -l"
##If user crontab does not exist returns a returncode of "42" and a message
#def getusercrontab(user):
#    
#    cronfile = '/var/spool/cron/crontabs/' + user
#
#    if not os.path.exists( cronfile ):
#        
#        #On user missing return getuser() error dictionary
#        userexists = getuser(user)
#        if not userexists['returncode'] is 0:
#            return command_error( returncode=41, stderr='No user found with name "' + user + '"' )
#        else:
#            return command_error( returncode=42, stderr='No crontab file found for user "' + user + '"' )
#
#    command = ['crontab', '-u', user, '-l']
#
#    try:
#        output = check_output(command, stderr=PIPE, universal_newlines=True)
#    except CalledProessError as e:
#        return command_error( e, command )
#
#    return command_success( data=output )
#
#
#def writeusercrontab( user, newcron, append=False ):
#    
#    #On user missing return getuser() error dictionary
#    userexists = getuser(user)
#    if not userexists['returncode'] is 0: return userexists
#
#    #Base variables
#    cronfile = '/var/spool/cron/crontabs/' + user
#    crontemp = '/tmp/tempcron'
#
#    with open(cronfile, 'r') as oldcron:
#        logid = mongolog( locals(), {'oldcron': 'ciao'} )
#        return command_success( data=oldcron.read() )
#        #logid = mongolog( locals(), {'oldcron': oldcron.read()} )
#
#    return command_success( data='OK' )
#
#    #Logging old and new crontab
#    #if os.path.isfile( cronfile ):
#        with open(cronfile, 'r') as oldcron:
#    #        return command_success( data=oldcron.read() )
#    #        logid = mongolog( locals(), {'oldcron': 'ciao'} )
#            logid = mongolog( locals(), {'oldcron': oldcron.read()} )
#    else:
#        logid = mongolog( locals(), {'oldcron': 'No old cron'} )
#
#
#    #If append is True: cron to write = old cron content + new cron content
#    if append:
#        oldcron = getusercron( user )
#        if not oldcron['returcode'] is 0: return oldcron
#        newcron = oldcron['data'] + newcron
#
#    with open( crontemp, 'w' ) as tempcron:
#        tempcron.write( newcron )
#
#    #Creating an empty crontab file for user "user"
#    command = 'crontab -u ' + user + ' - < ' + crontemp
#
#
#    try:
#        creation = check_output( command, shell=True )
#    except CalledProcessError as e:
#        return command_error( e, command )
#
#    return command_success( logid=logid )
