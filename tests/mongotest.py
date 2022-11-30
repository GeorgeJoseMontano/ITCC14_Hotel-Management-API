import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb://localhost:27017/itcc14?retryWrites=true&w=majority")
db = cluster["itcc14"]
collection = db["user_info"]



# biller = "water"
# amount = 1000


# # upsert
# collection.update_one({"_id": 102}, {"$set": {"bill."+biller:amount}}, upsert=True)

# # print all documents
# for x in collection.find():
#     print(x)

# # print a specific document
# print(collection.find_one({"_id": 101}))

# # print a specific field
# print(collection.find_one({"_id": 102}, {"bill":1}))

# # summ all bills
# print(collection.aggregate([{"$group": {"_id": None, "total": {"$sum": "$bill.water"}}}]))

# post = {'_id':108, 'fname':'George Jose', "guest_lname":"Montano", "email":"email@email.com", 
# "checkin":"2020-01-01", "checkout":"2020-01-02", "bill":{"electricity":1000, "water":2000}}
# collection.insert_one(post)

# # check if exists
# collection.find({"bill": {"$exists": True}})
# # check if exists and is not null
# collection.find({"bill": {"$exists": True, "$ne": None}})
# # check if exists for _id 101
# collection.find({"_id": 101, "bill": {"$exists": True, "$ne": None}})

# check if username and password exists and return user info
username = "test"
password = "test"
def test_user():
    return(collection.find_one({"username": username, "password": password})['_id'])


print(test_user())

