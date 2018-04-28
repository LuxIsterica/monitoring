# coding=utf-8
from subprocess import DEVNULL, PIPE, STDOUT, check_output, check_call, CalledProcessError
from utilities import mongolog, command_success, command_error
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
        return command_error(e, command, logid)

    return command_success(None)


def locate(name, insensitive=True):

    #Cannot search on empty string
    if not name:
        return { 'returncode': 255, 'stderr': 'Empty search string not allowed' }

    try:
        command = ['locate', '-i', name]
        if insensitive is False: command.pop(1)

        found = check_output(command, stderr=PIPE, universal_newlines=True).splitlines()
    except CalledProcessError as e:
        return command_error(e, command, logid)

    return command_success(found)


#Unlink file using his path
def removefile(path):

    logid = mongolog( locals() )

    try:
        os.remove(path)
    except OSError:
        pass

    return command_success(logid)
