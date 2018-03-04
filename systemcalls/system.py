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
#Information about cpu, memory and processes
def getsysteminfo( getall=True, getproc=False, getcpu=False, getmem=False ):

    try:
        command = ['cat', '/proc/meminfo'] #Getting memory information
        memraw = check_output(command, stderr=PIPE, universal_newlines=True).splitlines()
        command = ['cat', '/proc/cpuinfo'] #Getting cpu information
        cpuraw = check_output(command, stderr=PIPE, universal_newlines=True).splitlines()
        command = ['top', '-b', '-n1'] #Getting processes information
        procraw = check_output(command, stderr=PIPE, universal_newlines=True).splitlines()
    except CalledProcessError as e:
        return command_error(e, command)


    
    ##### CPU #####
    #Converting list() to set() to remove duplicate lines from output of command
    cpuraw = set(cpuraw) ##rIPRENDERE daQuI

    cpusetstripped = set()
    cpuset.add( ( re.sub('\t| ', '', line) ) for line in cpuset.pop() )
#    for line in cpuset:
#        cpusetstripped.add( re.sub('\t| ', '', line) )

    return cpuset

    #Deleting unwanted lines
    cpu = list()
    linestoremove = ('flags', 'apicid', 'processor', 'core id', 'coreid')

    for line in cpusetstripped:
        if not any(s in line for s in linestoremove):
            cpu.append(line)

    
    #### PROCESSES #####
    #Removing header from the output of top command
    i = 0
    while 'PID' not in procraw[i]: i+=1
    procraw = procraw[i:]

    #Getting header and splitting fields for use final dictionary keys
    keys = procraw.pop(0).lstrip()
    keys = keys.split()
    
    proc = list()

    for line in procraw:
        line = procraw.pop(0).lstrip()
        line = line.split()
        proc.append( dict( zip(keys, line) ) )




    ##### MEMORY #####
    #Inserting memory informations into info dictionary
    for line in memraw:
        line = re.sub(' ', '', line)
        line = line.split(':')
        infos.update( {line[0].lower() : line[1]} )


    #nproc
