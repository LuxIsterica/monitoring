# coding=utf-8
from subprocess import Popen, DEVNULL, PIPE, STDOUT, check_output, check_call, CalledProcessError
from utilities import mongolog, command_error
import os
import re
import datetime
import pprint
import inspect
#import urllib.parse

def updatedb():

    try:
        command = ['updatedb']
        check_call(command, stderr=PIPE)
    except CalledProcessError as e:
        return command_error(e, command)

    return 0


def locate(name, insensitive=True):

    try:
        command = ['locate', '-i', name]
        if insensitive is False: command.pop(1)

        found = check_output(command, stderr=PIPE, universal_newlines=True).splitlines()
    except CalledProcessError as e:
        return command_error(e, command)

    return found


#If "towrite" is not empty write the content into the file "filepath", else return the file contents
def getsetfile(filepath, towrite=""):

    if towrite:
        logid = mongolog( locals() )
        with open(filepath, 'w') as filedesc:
            filedesc.write(towrite)
        return logid
    else:
        with open(filepath, 'r') as filedesc:
            return filedesc.read()



#Unlink file using his path
def removefile(path):

    logid = mongolog( locals() )

    try:
        os.remove(path)
    except OSError:
        pass

    return logid
