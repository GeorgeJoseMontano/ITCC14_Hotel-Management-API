import pymongo
from pymongo import MongoClient

# Connect to the MongoDB, change the connection string per your MongoDB environment
cluster = MongoClient("mongodb://localhost:27017")
db = cluster["itcc14"]
guest_collection = db["guest_info"]
user_collection = db["user_info"]
bill_collection = db["bill_info"]
room_collection = db["room_info"]


