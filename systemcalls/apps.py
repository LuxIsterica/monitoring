# coding=utf-8
from subprocess import Popen, PIPE, STDOUT, check_output, check_call, CalledProcessError
from utilities import mongolog, command_error
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

    return logid



#Se icludesummary è True allora aggiunge alla lista restituita anche le informazioni sull'applicazione
def listinstalled( summary=False ):

    options = '-f=${binary:Package};${Version};${Architecture}' + ( ';${binary:Summary}\n' if summary else '\n' )
    command = ['dpkg-query', options, '-W']

    try:
        output = check_output(command, stderr=PIPE, universal_newlines=True).splitlines()
    except CalledProcessError as e:
        return command_error(e, command)
    except FileNotFoundError as e:
        return e


    #Lista di chiavi per le informazioni sull'app
    keys = ['name', 'version', 'architecture']
    if summary: keys.append('summary')
    
    #Conterrà una lista di dizionari con tutte le app installate nel sistema
    pkgs = list()

    #Inserimento valori nella lista apps()
    for i in output:
        appinfo = i.split(';')
        pkgs.append( dict( zip(keys, appinfo) ) )

    return pkgs



#Ricerca di una applicazione. se namesonly è true (default) la ricerca viene effettuata solo nel nome del pacchetto
def aptsearch( pkgname, namesonly=True ):

    command = ['apt-cache', 'search', pkgname]
    if namesonly: command.append('--names-only')

    output = Popen(command, stdout=PIPE, universal_newlines=True).communicate()[0].splitlines()

    keys = ['name', 'desc']
    pkgs = list()

    for i in output:
        appinfo = i.split(' - ')
        pkgs.append( dict( zip(keys, appinfo) ) )

    return pkgs


#A Lucia: verrà richiamato dopo aver fatto un search sui pacchetti installati o disponibili
#Mostra le informazioni sul pacchetto
#Returns: List
def aptshow(pkgname, onlydependences=False):
    
    mode = 'depends' if onlydependences else 'show'
    command = ['apt-cache', mode, pkgname]

    output = Popen(command, stdout=PIPE, universal_newlines=True).communicate()[0]
    
    #Se vengono restituiti più pacchetti (diverse versioni) prende solo il primo di questi
    if onlydependences:
        output = output.splitlines()
        output.pop(0) #Rimuove l'header
        output = [item.strip(' ') for item in output] #Rimuove gli spazi bianchi ad inizio e fine stringa
    else:
        output = output.split('\n\n')[0]
    
    return output
    


#A Lucia: Stampare messaggio che i pacchetti vengono installati non interattivamente
def aptinstall(pkgname):
    
    logid = mongolog( locals(), {'dependencies' : aptshow(pkgname,onlydependences=True)} )

    command = ['apt-get', 'install', '-y', pkgname]
    environ = {'DEBIAN_FRONTEND': 'noninteractive', 'PATH': os.environ.get('PATH')}

    try:
        check_call( command, env=environ )  #, stdout=open(os.devnull, 'wb'), stderr=STDOUT)
    except CalledProcessError:
        print( 'Errore durante l\'installazione del pacchetto "%s"' % (pkgname) )

    return logid



#A Lucia: checkbox "cancella tutto (purge)"
def aptremove(pkgname, purge=False):

    logid = mongolog( locals(), {'dependencies' : aptshow(pkgname,onlydependences=True)} )

    command = ['apt-get', 'purge' if purge else 'remove', '-y', pkgname]
    environ = {'DEBIAN_FRONTEND': 'noninteractive', 'PATH': os.environ.get('PATH')}

    try:
        check_call( command, env=environ ) #stdout=open(os.devnull, 'wb'), stderr=STDOUT)
    except CalledProcessError:
        print( 'Errore durante la rimozione del pacchetto "%s"' % (pkgname) )



def getexternalrepos():

    repospath = '/etc/apt/sources.list.d/'
    repos = list()

    try:
        command = ['ls', '-1', repospath]
        reposfiles = check_output(command, stderr=PIPE, universal_newlines=True).splitlines()

        lines = str()
        for filename in reposfiles:
            
            if not filename.endswith('.save'):
                with open(repospath + filename) as f:
                    lines = f.read()

                repos.append({
                    'filename': filename,
                    'lines': lines
                })

    except CalledProcessError as e:
        command_error(e, command)


    return repos



#returns <string> containing filename where repo is added
def addrepo(url, name):

    logid = mongolog( locals() )

    filename = '/etc/apt/sources.list.d/' + name + '.list'
    repofile = open( filename, 'a')
    repofile.write(url + '\n')
    repofile.close()

    return filename



def removerepofile(filename):

    logid = mongolog( locals() )

    repospath = '/etc/apt/sources.list.d/'

    try:
        os.remove(repospath + filename + '.list')
        os.remove(repospath + filename + '.list.save')
    except OSError:
        pass

    return logid
