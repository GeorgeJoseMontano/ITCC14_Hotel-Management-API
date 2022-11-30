import pymongo
from pymongo import MongoClient

# Connect to the MongoDB, change the connection string per your MongoDB environment
cluster = MongoClient("mongodb+srv://yoshilute:qH3tEc2mR2tw95Mr@cluster0.xx477oe.mongodb.net/?retryWrites=true&w=majority")
db = cluster["itcc14"]
guest_collection = db["guest_info"]
user_collection = db["user_info"]

