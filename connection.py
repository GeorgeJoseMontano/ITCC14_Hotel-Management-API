import pymongo
from pymongo import MongoClient

# Connect to the MongoDB, change the connection string per your MongoDB environment

db = cluster["itcc14"]
guest_collection = db["guest_info"]
user_collection = db["user_info"]

