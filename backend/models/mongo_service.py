from pymongo import MongoClient
from constant import *

def get_db():
    try:
        client = MongoClient(MONGODB_CONNECTION_STRING)
        db = client["ChatRoom"]
        return db
    except Exception as e:
        return {"error": "Error in Mongo Connection"}

database = get_db()
user_collection = database["users"]
