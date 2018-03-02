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
