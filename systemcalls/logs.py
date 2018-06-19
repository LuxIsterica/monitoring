# coding=utf-8
from subprocess import DEVNULL, PIPE, STDOUT, check_output, check_call, CalledProcessError
from utilities import mongolog, command_success, command_error, client, db
from pprint import pprint
import datetime
import dateutil.parser


#TODO: A Lucia: bisogna attivare la paginazione sui risultati
#TODO: A Lucia: sarebbe buono scegliere una data da un calendario
def getlog( objectid = None, funname = None, status = None, dategte = "1970-01-01", datelte = datetime.datetime.now().strftime("%Y-%m-%d") ):

    query = dict()
    dategte = dateutil.parser.parse( dategte )
    datelte = dateutil.parser.parse( datelte )

    if objectid:
        query = {"_id" : objectid }
    else:
        query.update({ "date": {"$gte": dategte, "$lte": datelte} })
        if funname: query.update({ "funname" : funname })
        if status: query.update({ "status": status })


    found = list()
    for log in db.log.find( query ):
        found.append( log )

    return command_success( data=found )
