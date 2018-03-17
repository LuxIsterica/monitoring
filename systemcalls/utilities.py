# coding=utf-8
from pymongo import MongoClient
import datetime
import pprint
import inspect
import hashlib


#Mongo Authenticationn
uri = "mongodb://root:test@localhost/admin?authMechanism=SCRAM-SHA-1"
client = MongoClient(uri)
db = client['nomodo']


#Logs operation to mongodb in the 'log' collection
#Should be called with locals() as first parameter
#args shuld be dict()
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
            return {'code': 2, 'message': 'Nothing to write(no changes from original file). If you wish to write anyway use the parameter "force=True"'}


    ##Execute this code just when Force==True or md5new != md5old
    #On different contents write to file
    logid = mongolog( locals() )
    opened = open(filename, 'w')
    opened.write(towrite)
    opened.close()
    return logid
