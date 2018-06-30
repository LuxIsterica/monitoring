# coding=utf-8
from subprocess import DEVNULL, PIPE, STDOUT, check_output, check_call, CalledProcessError
from utilities import mongolog, command_success, command_error
import os
import re
import datetime
import pprint
import inspect
#import urllib.parse


#If "newhostname" is not empty sets the hostname, else returns it
#Returnt tuple containing informtion about (cpu, mem, proc)
def hostname(newhostname=""):
    
    command = ['hostname']
        
    if newhostname:
        logid = mongolog( locals() )
        command.append(newhostname)

    try:
        hostname = check_output(command, stderr=PIPE, universal_newlines=True)
    except CalledProcessError as e:
        if newhostname:
            return command_error( e, command, logid )
        else:
            return command_error( e, command )

    if newhostname:
        return command_success( logid=logid )
    else:
        return command_success( data=hostname )


#Information about cpu, memory and processes
#Returns tuple
def getsysteminfo( getall=True, getproc=False, getcpu=False, getmem=False ):

    #Creating the tuple to return
    toreturn = ()


    #TODO
    ##### KERNEL E ARCH #####
    #uname -a
    #/etc/os-release




    ##### CPU #####
    if getall or getcpu:

        #Reading cpu stat from /opt files
        with open('/proc/cpuinfo', 'r') as cpuorig:
            cpuraw = cpuorig.read().splitlines()

        #Removing duplicate lines by converting list() to set()
        cpuraw = set(cpuraw)
        
        #Removing empty lines
        cpuraw = list( filter( None, cpuraw ) )
    
        #Removing useless lines
        linestoremove = ('flags', 'apicid', 'processor', 'core id', 'coreid')
        cpuraw = list( filter( lambda line: not any(s in line for s in linestoremove), cpuraw ) )
    
        #Deleting all tabulation and spaces for each line of the cpuraw set cpuraw
        cpuraw = map( lambda line: re.sub('[\t| ]*:[\t| ]*', ':', line), cpuraw )
    
    
        #We got three fields named "cpu Mhz", but to use them as dictionry keys
        #we need to rename them all
        cpuaf = list()
        i = 1
        for line in cpuraw:
            #Adds an incremental number to the key
            if 'mhz' in line.lower():
                cpuaf.append( re.sub('^.*:', 'core' + str(i) +' MHz:', line) )
                i += 1
            else: cpuaf.append( line )
    
    
        #Buiding final dictionary cotaining cpu information in the right form
        cpu = dict()
        for line in cpuaf:
            line = line.split(':')
            cpu.update({ line[0]: line[1] })

        #Adding cpu dict to the tuple to return
        toreturn = toreturn + (cpu,)





    ##### MEMORY #####
    if getall or getmem:

        #Reading memory status from /opt files
        with open('/proc/meminfo', 'r') as memorig:
            memraw = memorig.read().splitlines()


        #Filling mem dict with memory information
        mem = dict()
        for line in memraw:
            line = re.sub(' ', '', line)                #Removing spaces for each line
            line = line.split(':')                      #Splitting by colon
            mem.update({ line[0].lower() : line[1] })   #Appending the dictionary to a list to return

        toreturn = toreturn + (mem,)
    




    #### PROCESSES #####
    if getall or getproc:

        #Reading processes status using top command
        command = ['top', '-b', '-n1']

        try:
            procraw = check_output(command, stderr=PIPE, universal_newlines=True).splitlines()
        except CalledProcessError as e:
            return command_error( e, command )



        #Removing headers from the output of top command
        i = 0
        while 'PID' not in procraw[i]: i+=1
        procraw = procraw[i:]
        proc = list(map( lambda line: line.split(), procraw ))
        toreturn = toreturn + (proc,)
#           |_____________________________________________________________________ Real Value

#        procraw = procraw[i:]
#    
#        #Getting header and splitting fields for use final dictionary keys
#        keys = procraw.pop(0).lstrip()
#        keys = keys.split()
#        
#        proc = list()
#    
#        for line in procraw:
#            line = procraw.pop(0).lstrip()          #Removing initial spaces
#            line = line.split()                     #Splitting by spaces
#            proc.append( dict( zip(keys, line) ) )  #Creating a dictionary for each process and inserting into a list to return
#
#        toreturn = toreturn + (proc,)



    #dict, dict, list
    return command_success( data=toreturn )
