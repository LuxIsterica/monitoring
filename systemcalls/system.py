# coding=utf-8
from subprocess import Popen, PIPE, STDOUT, check_output, check_call, CalledProcessError
from utilities import mongolog, command_error
import os
import re
import datetime
import pprint
import inspect
#import urllib.parse


def hostname(hname=""):

    command = ['hostname']

    if hname:
        logid = mongolog( locals() )
        command.append(hname)

    try:
        hostname = check_output(command, stderr=PIPE, universal_newlines=True)
    except CalledProcessError as e:
        return command_error(e, command)

    return (logid if hname else hostname)


#Return a string the /etc/hosts file content
def gethosts():

    with open('/etc/hosts', 'r') as hostsfile:
        return hostsfile.read()


#TODO: mongolog
#Overwrite the /etc/hosts file with the one which the user
#has modified from the web interface
def writehosts(hosts):
    
    with open('hosts', 'w') as hostsfile:
        hostsfile.write(hosts)


#TODO: Only works on single cpu system
def getsysteminfo():

    try:
        command = ['cat', '/proc/meminfo']
        memraw = check_output(command, stderr=PIPE, universal_newlines=True).splitlines()
        command = ['cat', '/proc/cpuinfo']
        cpuraw = check_output(command, stderr=PIPE, universal_newlines=True).splitlines()
        command = ['top', '-b', '-n1']
        procraw = check_output(command, stderr=PIPE, universal_newlines=True).splitlines()
    except CalledProcessError as e:
        return command_error(e, command)


    
    #Using the set() instead of list() i can remove duplicate lines from results
    cpuset = set()
    for line in cpuraw: cpuset.add(line)

    cpusetstripped = set()
    for line in cpuset:
        cpusetstripped.add( re.sub('\t| ', '', line) )

    #Deleting unwanted lines
    cpu = list()
    linestoremove = ('flags', 'apicid', 'processor', 'core id', 'coreid')

    for line in cpusetstripped:
        if not any(s in line for s in linestoremove):
            cpu.append(line)

    
    #### PROCESSES #####
    #Removing header from the output of top command
    i = 0
    for i, line in enumerate(procraw):
        if 'PID' in line: break
    procraw = procraw[i:]

    #Fixing header line and splitting for fields for use as keys of the final dictionary
    keys = procraw.pop(0).lstrip()
    keys = re.sub('  *', ':', keys)
    keys = keys.split(':')
    
    proc = list()

    for line in procraw:
        proc.append( dict( zip(keys, procraw.pop(0)) ) )

    return proc


    infos = dict()

    #Inserting memory informations into info dictionary
    for line in memraw:
        line = re.sub(' ', '', line)
        line = line.split(':')
        infos.update( {line[0].lower() : line[1]} )


#    for line in cpu:



    #nproc
