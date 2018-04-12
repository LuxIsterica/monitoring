# coding=utf-8
from subprocess import DEVNULL, PIPE, STDOUT, check_output, check_call, CalledProcessError
from utilities import mongolog, command_success, command_error
import os
import re
import datetime
import pprint
import inspect
#import urllib.parse


#Returns dict
# @iface: if set only returns the stat of such interface
# @namesonly is needed in order to let "getnewifacealiasname" work properly
def ifacestat(iface="", namesonly=False):

    command = ['ifconfig', '-a']
    if iface: command.append(iface)

    try:
        output = check_output(command, stderr=PIPE, universal_newlines=True)
    except CalledProcessError as e:
        return command_error(e, command)


    #After this split each list item contains an interface specs
    output = output.split('\n\n')
    #Removing empty line at the end
    del output[-1]


    #List or dict to be returned
    #If namesonly=True is a list, dict instead
    ifaces = list() if namesonly else dict()
    for iface in output:

        #Splitting interface lines
        iface = iface.splitlines()

        #Getting iface name on first line
        #We need to split first line and reinsert the second item in the original list
        firstline = iface.pop(0).split(None, maxsplit=1)


        #Returns a list cotaining all interfaces name
        if namesonly:
            ifaces.append( firstline[0] )
        #Returns a dict containig all interfaces specs
        else:
            iface.insert(0, firstline[1])

            #Cutting out useless lines
            i = 0
            #Using "enumerate" because we need to modify the original list
            for index, value in enumerate(iface):
                #"i" indicates where to stop cutting
                i += 1
                #Removing leading and trailing spaces
                iface[index] = iface[index].strip()
                if iface[index].startswith('UP'): break


            #A dictionary where the key is the interface name and the value is part of the lines related to such interface
            ifaces.update({ firstline[0]: '\n'.join(iface[:i]) })


    return command_success( ifaces )


#Returns a string containing an alias name that fit to be used as alias for "iface" interface
# @iface interface name
# @Returns string
def getnewifacealiasname(iface):
    
    ifaces = ifacestat( iface=iface, namesonly=True )
    if ifaces['returncode'] is 0:
        ifaces = ifaces['data']

    occurrences = 0
    for item in ifaces:
        if item.startswith(iface):
            occurrences += 1

    return command_success( iface + ':' + str(occurrences) )



# Bring interface down or destroy alias
# @Returns logid
def ifacedown( iface ):
    
    logid = mongolog( locals() )

    command = ['ifconfig', iface, 'down']

    try:
        check_call(command)
    except CalledProcessError as e:
        return command_error(e, command)

    return command_success( logid )
    

"""
Bring interface up or create new alias if "iface" param does not correspond to any iface name.
On alias creation "iface" must be defined using "getnewifacealiasname" function
@Returns logid
"""
def ifaceup( iface, address="", netmask="", broadcast="" ):
    
    logid = mongolog( locals() )    

    command = ['ifconfig', iface]
    if address: command.append(address)
    if netmask: command = command + ['netmask', netmask]
    if broadcast: command = command + ['broadcast', broadcast]
    command.append('up')

    try:
        check_output = check_call(command, stderr=PIPE, universal_newlines=True)
    except CalledProcessError as e:
        return command_error(e, command)

    return command_success( logid )


"""
Functions to create or destroy alias. This functions use "ifaceup" and "ifacedown"
iface must be defined using "getnewifacealiasname" function
"""
def createalias( iface, address, netmask="", broadcast="" ):
    return ifaceup(iface=iface, address=address, netmask=netmask, broadcast=broadcast)
def destroyalias( iface ):
    return ifacedown( iface )


#discutere con Lucia della formattazione che deve essere simile a quella del comando
def getroutes():
    
    command = ['route', '-n']

    try:
        output = check_output(command, stderr=PIPE, universal_newlines=True).splitlines()
    except CalledProcessError as e:
        return command_error(e, command)


    #Removing useless header
    output.pop(0)

    #Storing useful header to use later
    header = output.pop(0).split()
    routes = list( map( lambda route: dict(zip(header, route.split())), output ) )


    return command_success( routes )


#Either add a route or set a default route on default=True
def addroute(gw, net, netmask, default=False):

    logid = mongolog( locals() )

    command = ['route', 'add']
    if default:
        command = command + ['default', 'gw', gw]
    elif net is None or netmask is None:
        raise ValueError('On non-default route you must enter "net" and "netmask" parameters')
    else:
        command = command + ['-net', net, 'netmask', netmask, 'gw', gw]

    try:
        check_call(command)
    except CalledProcessError as e:
        return command_error(e, command)

    return command_success(logid)


#Calls addroute with "default" paramemters on "True" and "None" on "net" and "netmask"
def defaultroute(gw): return addroute(gw, net=None, netmask=None, default=True) 


#TODO: Continue from here
def delroute(route):
    if isistance(route, dict):
        return command_success( 'dict' )
    else:
        return command_success( 'not_dict' )
