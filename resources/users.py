from parsers import user_parser
from connection import user_collection
from flask_restful import Resource
from key_gen import generate_key
from authorization import auth

class User_Register(Resource):
    # ✔️
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
                return "User registration successful", 200       
        except:
            return "There was an error registering user", 400
    # # ✔️ BUT DON'T USE THIS IS FOR TESTING PURPOSES ONLY
    # delete all users from the database
    def delete(self):
        try:
            user_collection.delete_many({})
            return "All users deleted", 200
        except:
            return "Error deleting user", 400
    

class User_Login(Resource):
    # ✔️
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
                return "User successfully logged in", 200
        except:
            return "Error logging in user", 400

class User(Resource):
    # change password
    @auth.login_required
    def patch(self):
        try:
            args = user_parser.parse_args()
            # check if username exists
            if user_collection.find_one({"username": args['username']}) is None:
                return "Username does not exist", 400
            # check if password is correct
            if user_collection.find_one({"username": args['username'], "password": args['password']}) is None:
                return "Incorrect password", 400
            else:
                user_collection.update_one({"username": args['username']}, {"$set": {"password":args['new_password']}})
                return "Password updated", 200
        except:
            return "Error updating password", 400

    @auth.login_required
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

    def get(self):
        try:
            args = user_parser.parse_args()
            # check if username exists
            if user_collection.find_one({"username": args['username']}) is None:
                return "Username does not exist", 400
            # check if password is correct
            if user_collection.find_one({"username": args['username'], "password": args['password']}) is None:
                return "Incorrect password", 400
            else:
                return user_collection.find_one({"username": args['username']}), 200
        except:
            return "Error getting user", 400
            