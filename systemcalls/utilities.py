from pymongo import MongoClient
import datetime
import pprint
import inspect


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



def mongoaddtodocument(logid, *fields)



#Deve essere chiamato quando viene lanciata una eccezione di tipo CalledProcessError
#Restituisce un dizionario con le informazioni sull'eccezione
def command_error(e, c):

    return dict({
        'returncode': e.returncode,
        'command': ' '.join(c),
        'stderr': e.stderr
    })
