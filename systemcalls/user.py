# coding=utf-8
from subprocess import Popen, PIPE, check_output, CalledProcessError, call, STDOUT
from utilities import mongolog, command_error
import re
#import urllib.parse



def getuser(user=None):

    try:
        command = ['getent', 'passwd',  user]
        userinfo = check_output(command, stderr=PIPE, universal_newlines=True).splitlines()

        command = ['groups', user]
        usergroups = check_output(command, stderr=PIPE, universal_newlines=True).splitlines()

    except CalledProcessError as e:
        return command_error(e, command)
    
    

    #Info sull'utente dal file /etc/passwd
    userinfo = userinfo[0].split(':')
    
    #Gruppi a cui l'utente appartiene
    usergroups = re.sub('^.*: ', '', usergroups[0])
    usergroups = usergroups.split(' ')
    
    
    return dict({
    	'uname': userinfo[0],
    	'canlogin': 'yes' if userinfo[1]=='x' else 'no',
    	'uid': userinfo[2],
    	'gid': userinfo[3],
    	'geco': userinfo[4].split(','),
    	'home': userinfo[5],
    	'shell': userinfo[6],
    	'group': usergroups.pop(0),
    	'groups': usergroups
    })



#Returns a list of dictionaries containing username ad userid of all system's users
def getusers():


    with open('/etc/passwd', 'r') as passwdorig:
        passwd = passwdorig.read().splitlines()


    users = list()
    for line in passwd:
        line = line.split(':', 3)
        users.append({
    	    'uname': line[0],
    	    'uid': line[2]
        })

    return users


    #p1 = Popen(["cat", "/etc/passwd"], stdout=PIPE)
    #output = Popen(["cut", "-d:", "-f4-", "--complement"], stdin=p1.stdout, stdout=PIPE, universal_newlines=True).communicate()[0].splitlines()
    #p1.stdout.close()
    ##universal newlines serve a restutuire l'output come stringa e non come bytes
    ##p3 = Popen(["sed", "s/:.:/:/g"], stdin=p2.stdout, stdout=PIPE, universal_newlines=True).communicate()[0] #, stdout=outputfile)
    ##p2.stdout.close()
    #
    #users = list()
    #for i in output:
    #	actual = i.split(':')
    #	users.append({
    #		'uname': actual[0],
    #		'uid': actual[2]
    #})
    #
    #return users
    
    
    #print(users)
    #print(*string, sep='\n')
    
    #for line in p1.stdout:
    #	print(line)
    #
    #p2.stdout.close()


def getgroups():

    with open('/etc/group', 'r') as grouporig:
        etcgroup = grouporig.read().splitlines()


    groups = list()
    for line in etcgroup:
        line = line.split(':')
        groups.append({
            'gname': line[0],
    	    'gid': line[2],
    	    'members': line[3].split(',')
    	})
    
    return groups


def addusertogroups(user, *groups):

    #Logging operation to mongo first
    logid = mongolog( locals(), getuser(user) )
    
    try:
    	for group in groups:
            command = ['adduser', user, group],
            check_output(command, stderr=PIPE, universal_newlines=True)
    except CalledProcessError as e:
        return command_error(e, command)
    
    
    #ObjectID of mongo
    return logid


def removeuserfromgroups(user, *groups):

    #Logging operation to mongo first
    logid = mongolog( locals(), getuser(user) )
    
    
    try:
    	for group in groups:
                command = ['gpasswd', '-d', user, group]
                check_output(command, stderr=PIPE, universal_newlines=True)
    except CalledProcessError as e:
        return command_error(e, command)
    
    
    #ObjectID of mongo
    return logid


def updateuserpass(user, password):

    #TODO: In questo modo la password viene memorizzata in mongo
    logid = ( locals() )
    
    try:
    	p1 = Popen(['echo', user + ':' + password], stdout=PIPE)
    	p2 = Popen(['/usr/sbin/chpasswd'], stdin=p1.stdout)
    	p1.stdout.close()
    
    except CalledProcessError:
    	print('Errore durante l\'aggiornamento della password dell\'utente %s' % (user))
    
    
    return logid



def updateusershell(user, shell):
	
    logid = mongolog( locals() )
    
    if not shell:
    	raise SyntaxError("La stringa contenente il nome della shell non può essere vuota")
    
    try:
        command = ['chsh', user, '-s', shell]
        check_output(command, stderr=PIPE, universal_newlines=True)
    except CalledProcessError as e:
        return command_error(e, command)

    
    return logid



#A Lucia: Inserire la shell di default nel form (a Lucia)
def adduser(user, password, shell="/bin/bash"):
	
    logid = mongolog( locals() )
    

    if not shell:
    	raise SyntaxError("La stringa contenente il nome della shell non può essere vuota")
    
    try:
        command = ['useradd', '-m', '-p', password, '-s', shell, user]
        check_output(command, stderr=PIPE, universal_newlines=True)
    except CalledProcessError as e:
        return command_error(e, command)
    

    return logid



def removeuser(user, removehome=None):
	
    logid = mongolog( locals(), getuser(user) )
    

    try:
        command = ['deluser', user]
        if removehome: command.append('--remove-home') 

        check_output( command, stderr=PIPE, universal_newlines=True )
    except CalledProcessError as e:
        return command_error(e, command)
    
    
    return logid
