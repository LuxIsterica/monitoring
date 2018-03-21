# coding=utf-8
from subprocess import PIPE, DEVNULL, STDOUT, check_output, check_call, CalledProcessError
from utilities import mongolog, command_success, command_error
import os
import re
import datetime
import pprint
import inspect
#import urllib.parse



def aptupdate():

    logid = mongolog( locals() )

    try:
        command = ['apt-get', 'update']
        check_call(command)
    except CalledProcessError as e:
        return command_error(e, command)

    return command_success(logid)



#Se icludesummary è True allora aggiunge alla lista restituita anche le informazioni sull'applicazione
def listinstalled( summary=False ):

    options = '-f=${binary:Package};${Version};${Architecture}' + ( ';${binary:Summary}\n' if summary else '\n' )
    command = ['dpkg-query', options, '-W']

    try:
        output = check_output(command, stderr=PIPE, universal_newlines=True).splitlines()
    except CalledProcessError as e:
        return command_error(e, command)
    except FileNotFoundError as e:
        return command_error(e, command)


    #Lista di chiavi per le informazioni sull'app
    keys = ['name', 'version', 'architecture']
    if summary: keys.append('summary')
    
    #Conterrà una lista di dizionari con tutte le app installate nel sistema
    pkgs = list()

    #Inserimento valori nella lista apps()
    for i in output:
        appinfo = i.split(';')
        pkgs.append( dict( zip(keys, appinfo) ) )

    return command_success(pkgs)



#Ricerca di una applicazione. se namesonly è true (default) la ricerca viene effettuata solo nel nome del pacchetto
def aptsearch( pkgname, namesonly=True ):

    command = ['apt-cache', 'search', pkgname]
    if namesonly: command.append('--names-only')

    try:
        output = check_output(command, stderr=PIPE, universal_newlines=True).splitlines()
    except CalledProcessError as e:
        return command_error(e, command)

    keys = ['name', 'desc']
    pkgs = list()

    for i in output:
        appinfo = i.split(' - ')
        pkgs.append( dict( zip(keys, appinfo) ) )

    return command_success(pkgs)


#A Lucia: verrà richiamato dopo aver fatto un search sui pacchetti installati o disponibili
#onclydependencies option is used from other functions in this same file
#Shows package information
#Returns: List
def aptshow(pkgname, onlydependences=False):
    
    mode = 'depends' if onlydependences else 'show'
    command = ['apt-cache', mode, pkgname]

    try:
        output = check_output(command, stderr=PIPE, universal_newlines=True)
    except CalledProcessError as e:
        return command_error(e, command)
    
    #Se vengono restituiti più pacchetti (diverse versioni) prende solo il primo di questi
    if onlydependences:
        #Remove the first line (header)
        toreturn = re.sub('^.*\\n', '', output)
    else:
        toreturn = output.split('\n\n')[0]
        
    return command_success(toreturn)
    


#A Lucia: Stampare messaggio che i pacchetti vengono installati non interattivamente
def aptinstall(pkgname):
    
    logid = mongolog( locals(), {'dependencies' : aptshow(pkgname,onlydependences=True)} )

    command = ['apt-get', 'install', '-y', pkgname]
    environ = {'DEBIAN_FRONTEND': 'noninteractive', 'PATH': os.environ.get('PATH')}

    try:
        check_call( command, env=environ )  #, stdout=open(os.devnull, 'wb'), stderr=STDOUT)
    except CalledProcessError:
        print( 'Errore durante l\'installazione del pacchetto "%s"' % (pkgname) )

    return command_success(logid)



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
        return command_error(e, command)
    
    return command_success(logid)


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

    return command_success(repos)



#returns <string> containing filename where repo is added
def addrepo(url, name):

    logid = mongolog( locals() )

    filename = '/etc/apt/sources.list.d/' + name + '.list'
    repofile = open( filename, 'a')
    repofile.write(url + '\n')
    repofile.close()

    return command_success(logid)



def removerepofile(filename):

    logid = mongolog( locals() )

    repospath = '/etc/apt/sources.list.d/'

    try:
        os.remove(repospath + filename + '.list')
        os.remove(repospath + filename + '.list.save')
    except OSError:
        pass

    return command_succes(logid)
