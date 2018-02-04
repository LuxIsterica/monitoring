# coding=utf-8
from subprocess import Popen, PIPE, check_output, CalledProcessError
from pymongo import MongoClient
import re
import datetime
import pprint
import inspect
#import urllib.parse

import ast


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

def aptshow(pkgname):
    
    command = ['apt-cache', 'show', pkgname]
    p1 = Popen(command, stdout=PIPE, universal_newlines=True).communicate()[0]

    return p1
    


def aptinstall(appname):
    pass

def aptremove(appname):
    pass

