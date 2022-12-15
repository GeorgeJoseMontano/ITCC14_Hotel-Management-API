from parsers import room_parser
from connection import room_collection, guest_collection
from flask_restful import Resource
from checks import check_null_room
from authorization import auth

class Rooms(Resource):
    # ✔️
    def get(self, room_id):
        try:
            return room_collection.find_one({"_id": room_id}), 200
        except:
            return "There was an error retrieving the room", 500

class Rooms_Admin(Resource):
    # ✔️
    @auth.login_required
    def post(self):
        try:
            args = room_parser.parse_args()
            # check if room has already been created
            if room_collection.find_one({"_id": args["room_id"]}) is not None:
                return "Room has already been created and is in the database"
            else:
                room_collection.insert_one({"_id": args["room_id"], 
                "room_type": args["room_type"],
                "room_price": args["room_price"],
                "room_available": args["room_available"],
                "number_of_beds": args["number_of_beds"],
                "mini_fridge": args["mini_fridge"],
                "tv": args["tv"],
                "ac": args["ac"],
                "wifi": args["wifi"],
                "breakfast": args["breakfast"]})
                return "Room created"
        except:
            return "There was an error while creating the room", 500
    # ✔️
    @auth.login_required
    def put(self):
        # change room details
        try:
            args = room_parser.parse_args()
            # check if room is in database
            if room_collection.find_one({"_id": args["room_id"]}) is None:
                return "Room cannot be updated because it is not in the database", 404
            else:
                doc = room_collection.find_one({"_id": args["room_id"]})
                check_null_room(args, doc)
                room_collection.update_one({"_id": args["room_id"]}, {"$set": {"room_type": args["room_type"],
                "room_price": args["room_price"],
                "room_available": args["room_available"],
                "number_of_beds": args["number_of_beds"],
                "mini_fridge": args["mini_fridge"],
                "tv": args["tv"],
                "ac": args["ac"],
                "wifi": args["wifi"],
                "breakfast": args["breakfast"]}})
                return "Updating room details was successful", 200
        except:
            return "There was an error while updating the room", 500
    # ✔️
    @auth.login_required
    def patch(self):
        # This is for changing room availability during maintenance
        try:
            args = room_parser.parse_args()
            # check if room exists in database
            if room_collection.find_one({"_id": args["room_id"]}) is None:
                return "Room cannot be updated because it is not in the database", 404
            # check if room is occupied
            if guest_collection.find_one({"_id": args["room_id"]}) is not None:
                return "Room cannot be updated because it is occupied", 404
            else:
                room_collection.update_one({"_id": args["room_id"]}, {"$set": {"room_available": args["room_available"]}})
                return "Updating room availability was successful", 200
        except:
            return "There was an error while updating the room's availability", 500


