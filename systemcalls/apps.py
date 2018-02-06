# coding=utf-8
from subprocess import Popen, PIPE, STDOUT, check_output, check_call, CalledProcessError
from mongolog import log
import os
import re
import datetime
import pprint
import inspect
#import urllib.parse



def aptupdate():
    pass

#Se icludesummary è True allora aggiunge alla lista restituita anche le informazioni sull'applicazione
def listinstalled( summary=False ):

    options = '-f=${binary:Package};${Version};${Architecture}' + ( ';${binary:Summary}\n' if summary else '\n' )
    command = ['dpkg-query', options, '-W']

    p1 = Popen(command, stdout=PIPE, universal_newlines=True).communicate()[0]
    output = p1.splitlines()


    #Lista di chiavi per le informazioni sull'app
    keys = ['name', 'version', 'architecture']
    if summary: keys.append('summary')
    
    #apps conterrà la lista di dizionari con tutte le app da restituire
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

    p1 = Popen(command, stdout=PIPE, universal_newlines=True).communicate()[0]
    output = p1.splitlines()

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
    
    logid = log( locals(), {'dependencies' : aptshow(pkgname,onlydependences=True)} )

    command = ['apt-get', 'install', '-y', pkgname]
    environ = {'DEBIAN_FRONTEND': 'noninteractive', 'PATH': os.environ.get('PATH')}

    try:
        check_call( command, env=environ )  #, stdout=open(os.devnull, 'wb'), stderr=STDOUT)
    except CalledProcessError:
        print( 'Errore durante l\'installazione del pacchetto "%s"' % (pkgname) )

    return logid


#A Lucia: checkbox "cancella tutto (purge)"
def aptremove(pkgname, purge=False):

    logid = log( locals(), {'dependencies' : aptshow(pkgname,onlydependences=True)} )

    command = ['apt-get', 'purge' if purge else 'remove', '-y', pkgname]
    environ = {'DEBIAN_FRONTEND': 'noninteractive', 'PATH': os.environ.get('PATH')}

    try:
        check_call( command, env=environ ) #stdout=open(os.devnull, 'wb'), stderr=STDOUT)
    except CalledProcessError:
        print( 'Errore durante la rimozione del pacchetto "%s"' % (pkgname) )
