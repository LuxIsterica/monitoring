# coding=utf-8
from subprocess import Popen, DEVNULL, PIPE, check_output, CalledProcessError, call, STDOUT
from utilities import mongolog, command_success, command_error
import re
#import urllib.parse



def getuser(user):

    try:
        command = ['getent', 'passwd',  user]
        userinfo = check_output(command, stderr=PIPE, universal_newlines=True).splitlines()
    except CalledProcessError as e:
        return command_error(e, command)
    

    #Info sull'utente dal file /etc/passwd
    userinfo = userinfo[0].split(':')


    #Getting user groups
    usergroups = getusergroups(user)
    if usergroups['returncode'] is 0:
        usergroups = usergroups['data']
    else:
        return usergroups


    return command_success( dict({
    	'uname': userinfo[0],
    	'canlogin': 'yes' if userinfo[1]=='x' else 'no',
    	'uid': userinfo[2],
    	'gid': userinfo[3],
    	'geco': userinfo[4].split(','),
    	'home': userinfo[5],
    	'shell': userinfo[6],
    	'group': usergroups.pop(0), #Main user group
    	'groups': usergroups if usergroups else "< No groups >"
    }) )
    
    

#Returns a list of dictionaries containing username ad userid of all system's users
def getusers():

    with open('/etc/passwd', 'r') as opened:
        passwd = opened.read().splitlines()


    users = list()
    for line in passwd:
        line = line.split(':', 3)
        users.append({
    	    'uname': line[0],
    	    'uid': line[2]
        })

    return command_success(users)


    #print(*string, sep='\n')
    


#Returns ---> If namesonly=True: a list of string (group names)
#        ---> If namesonly=False: a list of dict (groups information)
def getgroups(namesonly=False):

    with open('/etc/group', 'r') as opened:
        etcgroup = opened.read().splitlines()


    groups = list()
    if namesonly:
        groups = list(map( lambda line: line.split(':')[0], etcgroup ))
    else:
        for line in etcgroup:
            line = line.split(':')
            groups.append({
                'gname': line[0],
                'gid': line[2],
                'members': line[3].split(',')
            })
    
    return command_success( groups )


#Returns all groups which the user belong to
# @Returns list
def getusergroups(user):

    command = ['groups', user]
    
    try:
        usergroups = check_output(command, stderr=PIPE, universal_newlines=True).splitlines()
    except CalledProcessError as e:
        command_success(e, command)

#                   .------Removing username from list
#                   |                       .----------.
#                   V                       V          | 
    usergroups = re.sub('^.*: ', '', usergroups[0]) #Only first line contains the groups
    usergroups = usergroups.split(' ')

    return command_success( usergroups )


#Returns all groups that "user" isn't in
def getusernotgroups(user):
    
    #Getting all system groups
    groups = getgroups(namesonly=True)
    if groups['returncode'] is 0:
        groups = groups['data']
    else:
        return groups

    #Getting user specific groups
    usergroups = getusergroups(user)
    if usergroups['returncode'] is 0:
        usergroups = usergroups['data']
    else:
        return usergroups

    usernotgroup = list(filter( lambda group: not any(s in group for s in usergroups), groups ))

    return command_success( usernotgroup )


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

    return command_success(logid)


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
    return command_success(logid)


def updateuserpass(user, password):

    #We literally cannot store password in mongo log,
    #hence here we are removing password from locals()
    localsvar = locals()
    del localsvar['password']
    logid = mongolog( localsvar )
    
    try:
        command = ['echo', user + ':' + password]
        p1 = Popen(command, stdout=PIPE)
        command = ['/usr/sbin/chpasswd']
        p2 = Popen(command, stdin=p1.stdout)
        p1.stdout.close()
    
    except CalledProcessError as e:
        return command_error(e, command)
    
    
    return command_success(logid)



#Returns a list containing available shells
def getshells():

    with open('/etc/shells') as opened:
        shells = opened.read().splitlines()

    #Removing comment lines
    shells = list( filter( lambda shell: not shell.startswith('#'), shells) )

    #Manually Appending dummy shells
    shells = shells + ['/usr/sbin/nologin', '/bin/false']

    return command_success(shells)




def updateusershell(user, shell):
	
    logid = mongolog( locals() )
    
    #TODO
    if not shell:
    	raise SyntaxError("La stringa contenente il nome della shell non può essere vuota")

    command = ['chsh', user, '-s', shell]
    
    try:
        check_output(command, stderr=PIPE, universal_newlines=True)
    except CalledProcessError as e:
        return command_error(e, command)

    
    return command_success(logid)



#A Lucia: Inserire la shell di default nel form (a Lucia)
def adduser(user, password, shell="/bin/bash"):
	
    logid = mongolog( locals() )
    
    #TODO
    if not shell:
    	raise SyntaxError("La stringa contenente il nome della shell non può essere vuota")
    
    try:
        command = ['useradd', '-m', '-p', password, '-s', shell, user]
        check_output(command, stderr=PIPE, universal_newlines=True)
    except CalledProcessError as e:
        return command_error(e, command)
    

    return command_success(logid)


def removeuser(user, removehome=None):
	
    logid = mongolog( locals(), getuser(user) )
    

    try:
        command = ['deluser', user]
        if removehome: command.append('--remove-home') 

        check_output( command, stderr=PIPE, universal_newlines=True )
    except CalledProcessError as e:
        return command_error(e, command)
    
    
    return command_success(logid)
