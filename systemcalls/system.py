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
    cpuraw = set(cpuraw)
    #Removing empty lines
    cpuraw = list(filter(None, cpuraw))
    #Delete all tabulation and spaces for each line of the cpuraw set cpuraw
    cpuraw = map( lambda line: re.sub('[\t| ]*:[\t| ]*', ':', line), cpuraw )


    #Deleting unwanted lines
    cpulist = list()
    linestoremove = ('flags', 'apicid', 'processor', 'core id', 'coreid')

    for line in cpuraw:
        if not any(s in line for s in linestoremove):
            cpulist.append(line)


    #We got three fields named "cpu Mhz", but to use them ad dictionry keys
    #we need to rename them all
    cpu = list()
    i = 1
    for line in cpulist:
        #Adds an incremental number to the key
        if 'mhz' in line.lower():
            cpu.append( re.sub('^.*:', 'cpu' + str(i) +' MHz:', line) )
            i += 1
        else: cpu.append( line )
    #QUI



    

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
        line = procraw.pop(0).lstrip()          #Removing initial spaces
        line = line.split()                     #Splitting by spaces
        proc.append( dict( zip(keys, line) ) )  #Creating a dictionary for each process and inserting into a list to return




    ##### MEMORY #####
    #Inserting memory informations into info dictionary
    mem = list()
    for line in memraw:
        line = re.sub(' ', '', line)                #Removing spaces for each line
        line = line.split(':')                      #Splitting by colon
        mem.append( {line[0].lower() : line[1]} ) #Appending the dictionary to a list to return

    return (cpu, proc, mem)