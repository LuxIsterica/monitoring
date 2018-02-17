# coding=utf-8
from subprocess import Popen, PIPE, STDOUT, check_output, check_call, CalledProcessError
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


def removefile(path):

    logid = mongolog( locals() )

    try:
        os.remove(path)
    except OSError:
        pass

    return logid
