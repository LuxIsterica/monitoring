# coding=utf-8
from subprocess import PIPE, DEVNULL, STDOUT, check_output, check_call, CalledProcessError
from utilities import mongolog, command_success, command_error, filedel
import os
import re
import datetime
from pprint import pprint
import inspect
#import urllib.parse


externalreposdir = "/etc/apt/sources.list.d/"


def aptupdate():

    logid = mongolog( locals() )

    try:
        command = ['apt-get', 'update']
        check_call(command)
    except CalledProcessError as e:
        return command_error( e, command, logid )

    return command_success( logid=logid )



#Se icludesummary è True allora aggiunge alla lista restituita anche le informazioni sull'applicazione
def listinstalled( summary=False ):

    options = '-f=${binary:Package};${Version};${Architecture}' + ( ';${binary:Summary}\n' if summary else '\n' )
    command = ['dpkg-query', options, '-W']

    try:
        output = check_output(command, stderr=PIPE, universal_newlines=True).splitlines()
    except CalledProcessError as e:
        return command_error( e, command )
    except FileNotFoundError as e:
        return command_error( e, command )


    #Lista di chiavi per le informazioni sull'app
    keys = ['name', 'version', 'architecture']
    if summary: keys.append('summary')
    
    #Conterrà una lista di dizionari con tutte le app installate nel sistema
    pkgs = list()

    #Inserimento valori nella lista apps()
    for i in output:
        appinfo = i.split(';')
        pkgs.append( dict( zip(keys, appinfo) ) )

    return command_success( data=pkgs )



#Ricerca di una applicazione. se namesonly è true (default) la ricerca viene effettuata solo nel nome del pacchetto
def aptsearch( pkgname, namesonly=True ):

    #Cannot search on empty string
    if not pkgname:
        command_error( returncode=255, stderr='Empty search string not allowed' )


    command = ['apt-cache', 'search', pkgname]
    if namesonly: command.append('--names-only')

    try:
        output = check_output(command, stderr=PIPE, universal_newlines=True).splitlines()
    except CalledProcessError as e:
        return command_error( e, command )

    keys = ['name', 'desc']
    pkgs = list()

    for i in output:
        appinfo = i.split(' - ')
        pkgs.append( dict( zip(keys, appinfo) ) )

    return command_success( data=pkgs )


#A Lucia: verrà richiamato dopo aver fatto un search sui pacchetti installati o disponibili
#onclydependencies option is used from other functions in this same file
#Shows package information
#Returns: List
def aptshow(pkgname, onlydependences=False):
    
    mode = 'depends' if onlydependences else 'show'

    try:
        command = ['apt-cache', mode, pkgname]
        output = check_output(command, stderr=PIPE, universal_newlines=True)
    except CalledProcessError as e:
        return command_error( e, command )
    

    if onlydependences:
        #Remove the first line (header)
        toreturn = re.sub('^.*\\n', '', output)
    else:
        #On multiple results only keep the first one
        output = output.split('\n\n')[0]
        output = output.splitlines() #<-- We use splitlines() here because onlydependences does not need a split-lined output

        #Check whether the package is installed or not
        isinstalled = None
        try:
            command = ['dpkg', '-l', pkgname]
            check_call(command)
        except CalledProcessError as e:
            isinstalled = False
        if isinstalled is None: isinstalled = True
     
        #Removing useless lines
        linestomantain = ['Package:', 'Version:', 'Priority:', 'Section:', 'Origin:', 'Installed-Size:', 'Depends:', 'Description', ' ']
        output = list( filter( lambda line: any( line.startswith(s) for s in linestomantain), output ) ) 

        #Merging all of descrition lines
        i = 0
        n = len(output)

        while i < n:
            if output[i].startswith(' '):
                output[i-1] = output[i-1] + output[i] #<-- Merge lines
                del output[i] #<-- Delete current line
                n -= 1
            else:
                i += 1


        #Converting list to dictionary
        toreturn = dict()
        for line in output:
            dictelems = line.split(':', maxsplit=1)
            toreturn.update({ dictelems[0] : dictelems[1] })

        #Is this package installed?
        toreturn.update({ 'Intalled' : 1 if isinstalled else 0 })


    return command_success( data=toreturn )
    



#A Lucia: Stampare messaggio che i pacchetti vengono installati non interattivamente
def aptinstall(pkgname):
    
    logid = mongolog( locals(), {'dependencies' : aptshow(pkgname,onlydependences=True)} )

    command = ['apt-get', 'install', '-y', pkgname]
    environ = {'DEBIAN_FRONTEND': 'noninteractive', 'PATH': os.environ.get('PATH')}

    try:
        check_call( command, env=environ )  #, stdout=open(os.devnull, 'wb'), stderr=STDOUT)
    except CalledProcessError:
        return command_error( returncode=14, stderr='Package installation error. Package name: "'+pkgname+'"', logid=logid )

    return command_success( logid=logid )



#Allows user to remove system packages using apt-get remove.
#If purge == True then launch "apt-get remove --purge" instead
#A Lucia: checkbox "cancella tutto (purge)"
def aptremove(pkgname, purge=False):

    logid = mongolog( locals(), {'dependencies' : aptshow(pkgname,onlydependences=True)} )

    command = ['apt-get', 'purge' if purge else 'remove', '-y', pkgname]
    environ = {'DEBIAN_FRONTEND': 'noninteractive', 'PATH': os.environ.get('PATH')}

    try:
        check_call( command, env=environ ) #stdout=open(os.devnull, 'wb'), stderr=STDOUT)
    except CalledProcessError as e:
        return command_error( e, command, logid )
    
    return command_success( logid=logid )


#Returns external repos added to system in folder /etc/apt/sources.list.d/
def getexternalrepos():

    repospath = '/etc/apt/sources.list.d/'
    reposfiles = os.listdir(repospath)

    #Removing file that ends with '.save'
    reposfiles = list( filter( lambda item: not item.endswith('.save'), reposfiles ) )

    #List to return
    repos = list()
    for filename in reposfiles:
        with open(repospath + filename) as opened:
            repos.append({
                'filename': filename,
                'lines': opened.read()
            })

    return command_success( data=repos )

def getreponame(): return 'nomodo-' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')

#returns <string> containing filename where repo is added
def addrepo( content, name ):

    logid = mongolog( locals() )

    filename = '/etc/apt/sources.list.d/' + name + '.list'
    repofile = open( filename, 'a')
    repofile.write(content + '\n')
    repofile.close()

    return command_success( logid=logid )

def removerepofile(filename):

    result = filedel( externalreposdir + filename )['logid']
    filedel( externalreposdir + filename + '.save' ) #Ignores errors if file not exists ignoring return dictionary

    logid = mongolog( locals() )

    repospath = '/etc/apt/sources.list.d/'

    try:
        os.remove(repospath + filename + '.list')
        os.remove(repospath + filename + '.list.save')
    except FileNotFoundError:
        return command_error( returncode=10, stderr='File to remove not found: "'+repospath+'"', logid=logid )
        
    if result['returncode'] is 0:
        return command_succes( logid=logid )
    else:
        return result
