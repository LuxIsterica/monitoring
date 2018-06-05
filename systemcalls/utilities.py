# coding=utf-8
from subprocess import PIPE, STDOUT, Popen, check_output, check_call, CalledProcessError
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
import pprint
import inspect
import hashlib
import os


#Mongo Authenticationn
uri = "mongodb://root:test@localhost/admin?authMechanism=SCRAM-SHA-1"
client = MongoClient(uri)
db = client['nomodo']


#Logs operation to mongodb in the 'log' collection
#Should be called with locals() as first parameter
#                       
#                       .------- Must be dict(); will be added to mongodb log
#                       |
def mongolog(params, *args):

    dblog = dict({
    	'date': datetime.datetime.utcnow(),     #Operation date
    	'funname': inspect.stack()[1][3],       #Function name
    	'parameters': params,                   #Called function's parameters
    })
    
    for arg in args:
        dblog.update( arg )

    #ObjectID in mongodb
    return db.log.insert_one( dblog ).inserted_id
    

# Creates or updates the field 'status' into an existing mongolog 
#
#           .-----------------------------------------------------------------------------------------------.
#           v                                                                                               #
def mongologstatus(logid, status):                                                                          #
                                                                                                            #
    return db.log.update_one(                                                                               #
        {'_id': logid},                                                                                     #
        {'$set': { 'status' : status }},                                                                    #
        upsert=False                                                                                        #
        )                                                                                                   #
                                                                                                            #
def mongologstatuserr(logid, status='error'):                                                               #
    return mongologstatus(logid, status)  # >---------------------------------------------------------------^
def mongologstatussuc(logid, status='success'):                                                             #
    return mongologstatus(logid, status)  # >---------------------------------------------------------------^


#Called on command success
#Returns a nice returncode and the data
#"data" may containg mongo object id
def command_success( data=None, logid=None, returncode=0 ):

    if logid:
        mongologstatussuc( logid )

    return dict({
        'returncode': returncode,
        'data': data,
        'logid': logid
    })



#Called when a CalledProcessError is raised
#Returns a dict containing exception info
def command_error( e=None, command=[], logid=None, returncode=1, stderr='No messages defined for this error' ):

    if logid:
        mongologstatuserr( logid )
    
    return dict({
        'returncode': e.returncode if e and hasattr(e, 'returncode') else returncode,
        'command': ' '.join(command),
        'stderr': e.stderr if e and hasattr(e, 'stderr')  else stderr,
        'logid': logid
    })



#If newcontent has no value (is None) then return the file content
#else if force is True write "newcontent" into the file without check for changes else
#else if new and old content md5sum are different write new content into the file
#else let user know that file has not been written because no changes has been made
def writefile(filepath, newcontent=None, force=False):

    if not newcontent:
        try:
            with open(filepath, 'r') as content:
                return content.read()
        except FileNotFoundError:
            return command_error( returncode=10, stderr='No file found on path : "'+filepath+'"' )

    if not force:
        #If force is not specified then calculate md5sum to check whether the file has changed.
        #If file hasn't changed it is not written
        md5new = hashlib.md5()

        #(Referring encode()) To calculate md5sum string 'newcontent' needs to be converted into 'bite' format
        md5new.update( newcontent.encode() )
        md5new = md5new.hexdigest()

        #old file content md5sum 
        md5old = hashlib.md5( open( filepath, 'rb' ).read() ).hexdigest()

        if md5new == md5old:
            return command_error( returncode=2, stderr='Nothing to write(no changes from original file). You can force writing using the parameter "force=True"' )



    ##This code will get executed on either Force==True or md5new != md5old

    #Better insert the diff between the 2 files instead of full content, thus
    #we need to remove the parameter "newcontent" from "locals()" and pass the dict() returned by the filediff() function to mongolog()
    localsvar = locals()
    del localsvar['newcontent']
    logid = mongolog( localsvar, filediff(filepath, newcontent) )

    #Writing new content to "filepath" file
    opened = open(filepath, 'w')
    opened.write(newcontent)
    opened.close()

    return command_success( logid=logid )







#Execute diff bash command between 2 files and saves the result output to mongodb
#to keep tracking of file modifications.
#Returns a dict() that perfectly fit to be a parameter for mongolog() function
#
#             .------.------ Filepath or String
#             |      |
#             |      |
def filediff(filea, fileb):

    #If either filea or fileb is string then create a temp file and write to content
    #to make possible diff execution
    if not os.path.exists(filea):
        filecontent = filea
        filea = '/tmp/.nomodotempa'
        with open(filea, 'w') as opened:
            opened.write(filecontent)

    #N.B. Python's internal write function keeps current file owner

    if not os.path.exists(fileb):
        filecontent = fileb
        fileb = '/tmp/.nomodotempb'
        with open(fileb, 'w') as opened:
            opened.write(filecontent)

    command = ['diff', filea, fileb]

    #Must use Popen here because check_output fails to return stdout and stderr on exit code != 0
    output = Popen(command, stdout=PIPE, universal_newlines=True).communicate()[0]

    return {'filediff': output }



def delfile(path):

    logid = mongolog( locals() )

    try:
        os.remove( path )
    except FileNotFoundError:
        return command_error( returncode=10, stderr='File to remove not found: "'+path+'"' )

    return command_success( logid=logid )
