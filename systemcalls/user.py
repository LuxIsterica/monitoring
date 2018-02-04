# coding=utf-8
from subprocess import Popen, PIPE, check_output, CalledProcessError
from mongolog import log
import re
#import urllib.parse



def getuser(user=None):
    p1 = Popen(['getent', 'passwd',  user], stdout=PIPE, universal_newlines=True).communicate()[0]
    p2 = Popen(['groups', user], stdout=PIPE, universal_newlines=True).communicate()[0]
    
    #Info sull'utente dal file /etc/passwd
    userinfo = p1.splitlines()
    userinfo = userinfo[0].split(':')
    
    #Gruppi a cui l'utente appartiene
    usergroups = p2.splitlines()
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
	


def getusers():

    p1 = Popen(["cat", "/etc/passwd"], stdout=PIPE)
    p2 = Popen(["cut", "-d:", "-f4-", "--complement"], stdin=p1.stdout, stdout=PIPE, universal_newlines=True).communicate()[0]
    p1.stdout.close()
    #universal newlines serve a restutuire l'output come stringa e non come bytes
    #p3 = Popen(["sed", "s/:.:/:/g"], stdin=p2.stdout, stdout=PIPE, universal_newlines=True).communicate()[0] #, stdout=outputfile)
    #p2.stdout.close()
    
    output = p2.splitlines()
    
    users = list()
    for i in output:
    	actual = i.split(':')
    	users.append({
    		'uname': actual[0],
    		'uid': actual[2]
    })
    
    return users
    
    
    #print(users)
    #print(*string, sep='\n')
    
    #for line in p1.stdout:
    #	print(line)
    #
    #p2.stdout.close()


def getgroups():
    p1 = Popen(["cat", "/etc/group"], stdout=PIPE, universal_newlines=True).communicate()[0]
    
    output = p1.splitlines()
    
    groups = list()
    for i in output:
        actual = i.split(':')
        groups.append({
            'gname': actual[0],
    	    'gid': actual[2],
    	    'members': actual[3].split(',')
    	})
    
    return groups


def addusertogroups(user, *groups):

    #Logging operation to mongo first
    logid = log( locals(), getuser(user) )
    
    
    try:
    	for group in groups:
    		check_output(['adduser', user, group])
    
    except CalledProcessError:
    	print( 'Errore nell\'aggiunta dell\'utente %s al gruppo %s' % (user, group) )
    
    
    #ObjectID of mongo
    return logid


def removeuserfromgroups(user, *groups):

    #Logging operation to mongo first
    logid = log( locals(), getuser(user) )
    
    
    try:
    	for group in groups:
    		check_output(['gpasswd', '-d', user, group])
    
    except CalledProcessError:
    	print( 'Errore nella rimozione dell\'utente %s dal gruppo %s' % (user, group) )
    
    
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
	
    logid = log( locals() )
    
    if not shell:
    	raise SyntaxError("La stringa contenente il nome della shell non può essere vuota")
    
    try:
    	check_output(['chsh', user, '-s', shell])
    
    except CalledProcessError:
    	print('Errore durante lal creazione dell\'utente')
    
    return logid



#TODO: Inserire la shell di default nel form (a Lucia)
def adduser(user, password, shell="/bin/bash"):
	
    logid = log( locals() )
    
    if not shell:
    	raise SyntaxError("La stringa contenente il nome della shell non può essere vuota")
    
    try:
    	check_output(['useradd', '-m', '-p', password, '-s', shell, user])
    
    except CalledProcessError:
    	print('Errore durante la creazione dell\'utente')
    
    
    return logid


def removeuser(user, removehome=None):
	
    logid = log( locals(), getuser(user) )
    
    command = ['deluser', user]
    if removehome: command.append('--remove-home')
    
    try:
    	check_output( command )
    except CalledProcessError:
    	print('Errore durante la rimozione dell\'utente o della sua cartella home')
    
    
    return logid
