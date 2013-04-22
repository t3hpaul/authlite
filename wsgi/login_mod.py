#login module that works with the mongodb to check if users exists and to add users
from pymongo import Connection
#from pymongo import MongoClient
import bcrypt
from bson.json_util import dumps as mongo_dumps
from email_mod import fire_activate
import json
from bson.objectid import ObjectId

global connection_url
global db_username 
global db_password
global database 
global mongo_client
db_username = ''
db_password = ''
connection_url = "mongodb://%s:%s@/"%(db_username, db_password)
mongo_client = Connection(connection_url)
database = mongo_client.AuthFramework


#username, password, email, firstname, lastname
def check_user_exists(username):
	collection = database.userPeople
	print collection.find({"username":username}).count()
	if collection.find({"username":username}).count() != 0:
		return True
	else:
		return False

#creates a user
def new_user(username, name, email, password):
	collection = database.userPeople
	password = bcrypt.hashpw(password, bcrypt.gensalt(10))
	collection.insert({"username":username,"password":password,"name":name,"email":email,"active":False})
	userinfo = collection.find_one({"username":username})
	oid = userinfo['_id']
	fire_activate(username, email, oid)

#updates the password
def update_pass(username,oid,password):
	collection = database.userPeople
        password = bcrypt.hashpw(password, bcrypt.gensalt(10))
	collection.update({"_id":ObjectId(oid)},{"$set":{"active":True,"password":password}})

def auth_user(username, password):
	auth = False
	collection = database.userPeople
	results = collection.find({"username":username})
	for thing in results:
		results = json.loads(mongo_dumps(thing))
		print results

	hash = results['password']
	if bcrypt.hashpw(password, hash) == hash and results['active']:
		auth = True
	return auth

def activate_user(oid):
	collection = database.userPeople
        collection.update({"_id":ObjectId(oid)},{"$set":{"active":True}})

def gen_rnd_id():
	import random
	randid = random.randint(0,99999)
	return randid

def create_user(username, password, email , firstname, lastname):
	created = False
	return created

def modify_user(username, password, email , firstname, lastname):
	modified = False
	return modified

#sets the account as inactive and
def set_inactive(username):
	collection = database.userPeople
        collection.update({"username":username},{"$set":{"active":False}})


#checks to see if the username and email are associated
def check_user_email(username,email):
	collection = database.userPeople
	user_results = collection.find_one({"username":username})
	if len(user_results) == 0:
		return False
	else:
		if user_results['email'] == email:
			return user_results["_id"]
		else:
			return False
