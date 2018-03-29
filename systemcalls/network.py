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


def getnewifacealiasname(iface):
    
    ifaces = ifacestat( iface=iface, namesonly=True )
    if ifaces['returncode'] is 0:
        ifaces = ifaces['data']

    occurrences = 0
    for item in ifaces:
        if item.startswith(iface):
            occurrences += 1

    return command_success( iface + ':' + str(occurrences) )


def addifacealias(newname):
    pass
