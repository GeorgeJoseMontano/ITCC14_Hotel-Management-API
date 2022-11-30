from bson import ObjectId
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from key_gen import generate_key
from connection import guest_collection, user_collection
from parsers import guest_parser, user_parser, del_user_parser

app = Flask(__name__)
api = Api(app)

# Operations available for public
class Guest_Public(Resource):
    # ✔️
    # get guest information in room
    def get(self, room_id):
        try:
            args = del_user_parser.parse_args()
            # check if key is valid
            if check_key(args['key']) == False:
                return "Error: Invalid key.", 400
            if guest_collection.find_one({"_id": room_id}) is None:
                return "Error: Room not occupied", 400
            else:
                #return guest information for that room
                return jsonify(guest_collection.find_one({"_id": room_id}))
        except:
            return "Error: Room not available, unoccupied, or no key was provided", 404
    # ✔️
    # book guest into a room
    def post(self, room_id):
        try:
            args = guest_parser.parse_args()
            # check if key is valid
            if check_key(args['key']) == False:
                return "Error: Invalid key", 400
            # check if room is occupied
            if guest_collection.find_one({"_id": room_id}) is not None:
                return "Error: Room occupied", 400
            else:
                post = {'_id':room_id, 
                    'fname':args['fname'], 
                    "lname":args['lname'], 
                    "email":args['email'], 
                    "checkin":args['checkin'], 
                    "checkout":args['checkout'],
                    # "bill":args['bill']
                    }
                guest_collection.insert_one(post)
                # guest_collection.update_one({"_id": room_id}, {"$set": {"bill":{}}}, upsert=True)
                return "Guest checked in", 201
        except:
            return "Error adding guest", 400
    # ✔️
    # check out a guest from a room
    def delete(self, room_id):
        try:
            args = del_user_parser.parse_args()
            # check if key is valid
            if check_key(args['key']) == False:
                return "Error: Invalid key", 400
            # check if room is occupied
            if guest_collection.find_one({"_id": room_id}) is None:
                return "Error: Room not occupied", 400
            # add a check bill database if guest has bill
            else:
                guest_collection.delete_one({"_id": room_id})
                return "Guest checked out", 200
        except:
            return "Error: Room not available or unoccupied", 404
    # ✔️
    # Move guest to a new room or update guest information
    def put(self, room_id):
        try:
            args = guest_parser.parse_args()
            # check if key is valid
            if check_key(args['key']) == False:
                return "Error: Invalid key", 400
            # check if room is occupied
            if guest_collection.find_one({"_id": room_id}) is None:
                return "Error: Room not occupied", 400
            if args['room_id'] is not None:
                # move guest to a new room (may have to make new url for this instead)
                doc = guest_collection.find_one({"_id": room_id})
                doc['_id'] = args['room_id']
                guest_collection.insert_one(doc)
                guest_collection.delete_one({"_id": room_id})
                return "Guest moved to new room", 200
            else:
                # update guest information
                guest_collection.update_one({"_id": room_id}, {"$set": {"fname":args['fname'], "lname":args['lname'], 
                "email":args['email'], "checkin":args['checkin'], "checkout":args['checkout']}})
                return "Guest information updated", 200
        except:
            return "Error updating guest information", 400 

# Note to Self - I think we should remove post, delete, and put from guest

# Admin operations for managers only
class Guest_Admin(Resource):
    # ✔️
    # get a specific guest information or all guests from the database
    def get(self):
        try:
            args = del_user_parser.parse_args()
            get_info = guest_collection.find()
            # check if key is valid
            if check_key(args['key']) == False:
                return "Error: Invalid key", 400
            # check if args['room_id'] is empty
            if args['room_id'] is not None and guest_collection.find_one({"_id": args['room_id']}) is not None:
                return guest_collection.find_one({"_id": args['room_id']}), 200
            else:
                return [x for x in get_info], 200
        except:
            return "Error: No guests in database", 404   
    # ✔️
    # book a guest into a room
    def post(self):
        try:
            args = guest_parser.parse_args()
            # check if key is valid
            if check_key(args['key']) == False:
                return "Error: Invalid key", 400
            # check parameters if empty
            if check_parameters(args) == False or args['room_id'] is None:            
                return "Error: Incomplete guest details", 400
            #check if args['room_id'] is empty
            
            # check if room is occupied
            if guest_collection.find_one({"_id": args['room_id']}) is not None:
                return "Error: Room occupied", 400
            else:
                post = {'_id':args['room_id'], 
                    'fname':args['fname'], 
                    "lname":args['lname'], 
                    "email":args['email'], 
                    "checkin":args['checkin'], 
                    "checkout":args['checkout']}
                guest_collection.insert_one(post)
                return "Guest checked in", 201                
        except:
            return "Error adding guest", 400
    # ✔️
    # delete a guest or all guests from the database
    def delete(self):
        try:
            args = del_user_parser.parse_args()
            # check if key is valid
            if check_key(args['key']) == False:
                return "Error: Invalid key", 400
            # check if args['room_id'] is empty
            if args['room_id'] is None and args['room_id'] == 999:
                return "Error: Room ID is required", 400
            # check if room is occupied
            if guest_collection.find_one({"_id": args['room_id']}) is None and args['room_id'] != 999:
                return "Error: Room not occupied", 400
            # check if admin wants to delete all or one
            if args['room_id'] == 999:
                guest_collection.delete_many({})
                return "All guests checked out", 200
            else:
                guest_collection.delete_one({"_id": args['room_id']})
                return "Guest checked out", 200 
        except:
            return "Error checking out guests", 400
    # ✔️
    # Move guest to a new room or update guest information
    def put(self):
        try:
            args = guest_parser.parse_args()
            # check if key is valid
            if check_key(args['key']) == False:
                return "Error: Invalid key", 400
            # check if new room is occupied
            if guest_collection.find_one({"_id": args['new_id']}) is not None and args['new_id'] != args['room_id']:
                return "Error: Room occupied", 400
            # check if old room is occupied
            if guest_collection.find_one({"_id": args['room_id']}) is None:
                return "Error: There are no guests to move", 400
            # move guest to a new room
            if args['new_id'] is not None:
                doc = guest_collection.find_one({"_id": args['room_id']})
                doc['_id'] = args['new_id']
                guest_collection.insert_one(doc)
                guest_collection.delete_one({"_id": args['room_id']})
                return "Guest moved to new room", 200
            # update guest information
            else:      
                doc = guest_collection.find_one({"_id": args['room_id']})
                check_null(args, doc)  
                guest_collection.update_one({"_id": args['room_id']}, {"$set": {"fname":args['fname'], "lname":args['lname'], 
                "email":args['email'], "checkin":args['checkin'], "checkout":args['checkout']}})
                return "Guest information updated", 200
        except:
            return "Error updating guest information", 400         

class User_Register(Resource):
    def post(self):
        try:
            args = user_parser.parse_args()
            key = generate_key()
            post = {'_id':key, 'username':args['username'], 'password':args['password']}
            # check if username already exists
            if user_collection.find_one({"username": args['username']}) is not None:
                return "Username already exists", 400  
            else:
                user_collection.insert_one(post)
                return user_collection.find({"username": args['username']})[0], 201
                         
        except:
            return "Error adding user", 400

    # delete all users from the database
    def delete(self):
        try:
            args = del_user_parser.parse_args()
            # check if key is valid
            if check_key(args['key']) == False:
                return "Error: Invalid key", 400
            else:
                user_collection.delete_many({})
                return "All users deleted", 200
        except:
            return "Error deleting user", 400

class User_Login(Resource):
    def post(self):
        try:
            args = user_parser.parse_args()
            # check if username exists
            if user_collection.find_one({"username": args['username']}) is None:
                return "Username does not exist", 400
            # check if password is correct
            if user_collection.find_one({"username": args['username'], "password": args['password']}) is None:
                return "Incorrect password", 400
            else:
                return str(user_collection.find_one({"username": args['username'], "password": args['password']})["_id"])
        except:
            return "Error logging in user", 400

    # change password
    def put(self):
        try:
            args = user_parser.parse_args()
            # check if username exists
            if user_collection.find_one({"username": args['username']}) is None:
                return "Username does not exist", 400
            # check if password is correct
            if user_collection.find_one({"username": args['username'], "password": args['password']}) is None:
                return "Incorrect password", 400
            else:
                user_collection.update({"username": args['username']}, {"$set": {"password":args['new_password']}})
                return "Password updated", 200
        except:
            return "Error updating password", 400

    # delete user
    def delete(self):
        try:
            args = user_parser.parse_args()
            # check if username exists
            if user_collection.find_one({"username": args['username']}) is None:
                return "Username does not exist", 400
            # check if password is correct
            if user_collection.find_one({"username": args['username'], "password": args['password']}) is None:
                return "Incorrect password", 400
            else:
                user_collection.delete_one({"username": args['username']})
                return "User deleted", 200
        except:
            return "Error deleting user", 400


    def post(self):
        try:
            args = bill_parser.parse_args()
            # check if key is valid
            if check_key(args['key']) == False:
                return "Error: Invalid key", 400
            # check if room is occupied
            if guest_collection.find_one({"_id": args['room_id']}) is None:
                return "Error: Room not occupied", 400
            # check if bill already exists
            if bill_collection.find_one({"room_id": args['room_id']}) is not None:
                return "Error: Bill already exists", 400
            else:
                post = {'room_id':args['room_id'], 'bill':args['bill']}
                bill_collection.insert_one(post)
                return bill_collection.find_one({"room_id": args['room_id']}), 201
        except:
            return "Error adding bill", 400

api. add_resource(Guest_Public, '/guest/<int:room_id>')
api. add_resource(Guest_Admin, '/guest')
api. add_resource(User_Register, '/user/register')
api. add_resource(User_Login, '/user/login')

# check if user key is valid
def check_key(key):
        if user_collection.find_one({"_id": key}) is not None:
            return True
        else:
            return False

# check if any fields are null
def check_parameters(args):
    if args['fname'] is None or args['lname'] is None or args['email'] is None or args['checkin'] is None or args['checkout'] is None:
        return False
    else:
        return True

# check for null values in args and replace with old values
def check_null(args, doc):
    if args['fname'] is None:
        args['fname'] = doc['fname']
    if args['lname'] is None:
        args['lname'] = doc['lname']
    if args['email'] is None:
        args['email'] = doc['email']
    if args['checkin'] is None:
        args['checkin'] = doc['checkin']
    if args['checkout'] is None:
        args['checkout'] = doc['checkout']

if __name__ == '__main__':
    app.run(debug=True)
