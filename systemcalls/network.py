# coding=utf-8
from subprocess import DEVNULL, PIPE, STDOUT, check_output, check_call, CalledProcessError
from utilities import mongolog, command_success, command_error
import inspect
import re
#import urllib.parse


'''
@iface: if set only returns the stat of such interface
@namesonly is needed in order to let "getnewifacealiasname" work properly
>Returns dict
'''
def ifacestat(iface="", namesonly=False):

    command = ['ifconfig', '-a']
    if iface: command.append(iface)

    try:
        output = check_output(command, stderr=PIPE, universal_newlines=True)
    except CalledProcessError as e:
        return command_error( e, command )


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
                if iface[index].startswith('UP') or iface[index].startswith('DOWN'):  break


            #A dictionary where the key is the interface name and the value is part of the lines related to such interface
            ifaces.update({ firstline[0]: iface[:i] }) #  '\n'.join(iface[:i]) })


    return command_success( data=ifaces )


'''
@iface interface name
>Returns a string containing an alias name that fit to be used as alias for "iface" interface
'''
def getnewifacealiasname(iface):
    
    ifaces = ifacestat( namesonly=True )
    if ifaces['returncode'] is 0:
        ifaces = ifaces['data']

    
    aliasid = 0
    for item in ifaces:
        if item.startswith( iface + ':' ): #By default aliases will be parsed in numeric ascending order due to ifconfig output
            item = int(re.sub('.*:', '', item))
            if aliasid is item: aliasid += 1
            else: break

    return command_success( data = iface + ':' + str(aliasid) )
    



'''
Bring interface down or destroy alias
@iface interface name to bring down
>Returns logid
'''
def ifacedown( iface ):
    
    logid = mongolog( locals() )

    command = ['ifconfig', iface, 'down']

    try:
        check_call(command)
    except CalledProcessError as e:
        return command_error( e, command, logid )

    return command_success( logid=logid )
    

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
        return command_error( e, command, logid )

    return command_success( logid=logid )


"""
Functions to create or destroy alias. This functions use "ifaceup" and "ifacedown"
iface must be defined using "getnewifacealiasname" function
"""
def createalias( aliasname, address, netmask="", broadcast="" ):

    #Turning alias name into main interface name
    iface = re.sub(':.*', '', aliasname)

    #Check wether "iface" is a real interface
    aliases = ifacestat( namesonly=True )
    if aliases['returncode'] is 0:
        if not iface in aliases['data']:
            return command_error( returncode=197, stderr="No interface found with such name: " + iface )
    else:
        return aliases

    return ifaceup( iface=aliasname, address=address, netmask=netmask, broadcast=broadcast )


def destroyalias( aliasname ):
    return ifacedown( aliasname )
def editiface( iface, address="", netmask="", broadcast="" ):
    return ifaceup( iface=iface, address=address, netmask=netmask, broadcast=broadcast ) 


#discutere con Lucia della formattazione che deve essere simile a quella del comando
def getroutes():
    
    command = ['route', '-n']

    try:
        output = check_output(command, stderr=PIPE, universal_newlines=True).splitlines()
    except CalledProcessError as e:
        return command_error( e, command )


    #Removing useless header
    output.pop(0)

    #Storing useful header to use later
    header = output.pop(0).split()
    routes = list( map( lambda route: dict(zip(header, route.split())), output ) )


    return command_success( data=routes )


#Either add a route or set a default route on default=True
def addroute(gw, net, netmask, default=False):

    logid = mongolog( locals() )

    command = ['route', 'add']
    #If default is true we just need "gw" parameters
    if default:
        command = command + ['default', 'gw', gw]
    #If default in False "net" and "netmask" must be set
    elif net is None or netmask is None:
        command_error( returncode=201, stderr='On non-default route you must enter "net" and "netmask" parameters' )
    else:
        command = command + ['-net', net, 'netmask', netmask, 'gw', gw]

    try:
        check_call(command)
    except CalledProcessError as e:
        return command_error( e, command, logid )

    return command_success( logid=logid )


#Calls addroute with "default" paramemters on "True" and "None" on "net" and "netmask"
def defaultroute(gw): return addroute(gw, net=None, netmask=None, default=True) 


#route dict() must contain same keys of the dict() returned by getroutes() function
def delroute(route):

    logid = mongolog( locals() )

    if not type(route) is type(dict()):
        command_error( returncode=202, stderr='delroute function can only accept a dictionary as argument', logid=logid )

    command = [ 'route', 'del', '-net', route['Destination'], 'netmask', route['Genmask'], 'gw', route['Gateway'] ]

    try:
        check_call(command)
    except CalledProcessError as e:
        return command_error( e, command, logid )

    return command_success( logid=logid )
