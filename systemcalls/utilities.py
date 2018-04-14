# coding=utf-8
from subprocess import PIPE, STDOUT, Popen, check_output, check_call, CalledProcessError
from pymongo import MongoClient
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
#                       .------- Must be dict(); will be added to the log in mongodb
#                       |
def mongolog(params, *args):

    dblog = dict({
    	'date': datetime.datetime.utcnow(),     #Operation date
    	'funname': inspect.stack()[1][3],       #Function name
    	'parameters': params
    })
    
    for arg in args:
        dblog.update( arg )

    #ObjectID in mongodb
    return db.log.insert_one( dblog )
    
    
    #       #show collections
    #       print(db.collection_names(include_system_collections=False))
    #
    #       pprint.pprint(db.posts.find_one({"author":"Mike"}))



#def mongoaddtodocument(logid, *fields)
#    pass



#Called on command success
#Returns a nice returncode and the data
#"data" may containg mongo object id
def command_success( data=None, returncode=0 ):
    return dict({
        'returncode': returncode,
        'data': data
    })


#Called when a CalledProcessError is raised
#Returns a dict containing exception info
def command_error(e, c):

    return dict({
        'returncode': e.returncode,
        'command': ' '.join(c),
        'stderr': e.stderr
    })



#If towrite has no value (is None) then return the file content
#else if force is True write "towrite" into the file without check for changes else
#else if new and old content md5sum are different write new content into the file
#else let user know that file has not been written because no changes has been made
def filedit(filename, towrite=None, force=False):

    if not towrite:
        with open(filename, 'r') as opened:
            return opened.read()

    if not force:
        #If force is not specified then calculate md5sum to check if the file has changed.
        #If file hasn't changed it is notg written
        md5new = hashlib.md5()

        #(Referring encode()) To calculate md5sum string 'towrite' needs to be converted into 'bite' format
        md5new.update( towrite.encode() )
        md5new = md5new.hexdigest()

        #old file content md5sum 
        md5old = hashlib.md5( open( filename, 'rb' ).read() ).hexdigest()

        if md5new == md5old:

            #A modified version of the dict() returned from the function commans_success() which is quite used
            #Here stderr is a message so we assign it two keys
            return dict({
                'returncode': 2,
                ('message', 'stderr'): 'Nothing to write(no changes from original file). You can force writing using the parameter "force=True"'
            })



    ##This code is being executed on either Force==True or md5new != md5old

    #Better insert the diff between the 2 file instead of full content, thus
    #we need to remove the parameter "towrite" from "locals()" and pass the dict() returned by the filediff() function to mongolog()
    localsvar = locals()
    del localsvar['towrite']
    return filediff(filename, towrite)
    logid = mongolog( localsvar, filediff(filename, towrite) )
    opened = open(filename, 'w')

    opened.write(towrite)
    opened.close()

    return command_success(logid)






#Execute diff bash command between 2 files and saves the result output to mongodb
#to keep tracking of file modifications.
#Returns a dict() that perfectly fit to be a parameter for mongolog() function
#
#             .------.------ Filepath or String
#             |      |
#             |      |
def filediff(filea, fileb):

    #If either filea or fileb is tring then create a temp file and write to content
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
