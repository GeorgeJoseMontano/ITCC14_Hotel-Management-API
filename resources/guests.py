from parsers import guest_parser, del_user_parser
from connection import guest_collection
from flask_restful import Resource
from checks import check_parameters, check_null, check_room_status, check_total, start_bill, bill_change_room
from .bills import Bill
from authorization import auth

# Operations available for public
class Guest_Public(Resource):
    # ✔️
    # get guest information in room
    def get(self, room_id):
        try:
            guest_total
            return guest_collection.find_one({"_id": room_id}), 200

        except:
            return "Error: Room not available or unoccupied", 404

# Admin operations for managers only
class Guest_Admin(Resource):
    # ✔️
    # get a specific guest information or all guests from the database
    @auth.login_required
    def get(self):
        try:
            args = del_user_parser.parse_args()
            get_info = guest_collection.find()
            # check if args['room_id'] is empty
            if args['room_id'] is not None and guest_collection.find_one({"_id": args['room_id']}) is not None:
                guest_collection.update_one({"_id": args['room_id']}, {"$set": {"total": check_total(args['room_id'])}})
                return guest_collection.find_one({"_id": args['room_id']}), 200
            else:
                return [x for x in get_info], 200
        except:
            return "Error: No guests in database", 404  
    # ✔️
    # book a guest into a room
    @auth.login_required 
    def post(self):
        try:
            args = guest_parser.parse_args()
            # check if parameters are null or empty
            if check_parameters(args) == False or args['room_id'] is None:            
                return "Error: Incomplete guest details", 400
            # check if room is under maintenance
            if check_room_status(args['room_id']) == False:
                return "Error: Room is under maintenance", 400
            # check if room is currently occupied
            if guest_collection.find_one({"_id": args['room_id']}) is not None:
                return "Error cannot book room: Room is occupied", 400
            else:
                post = {'_id':args['room_id'], 
                    'fname':args['fname'], 
                    "lname":args['lname'], 
                    "email":args['email'],
                    "phone":args['phone'],
                    "num_guest":args['num_guest'], 
                    "checkin":args['checkin'], 
                    "checkout":args['checkout'],
                    "total":0}
                guest_collection.insert_one(post)
                # create initial bill
                Bill().initial_bill(args['room_id'],start_bill(args['room_id']),args['checkin'])
                guest_total(args['room_id'])
                return "Guest has been booked into room successfully", 200
        except:
            return "There was an error in booking the guest", 500
    # ✔️
    # delete a guest or all guests from the database
    @auth.login_required
    def delete(self):
        try:
            args = del_user_parser.parse_args()
            # check if args['room_id'] is empty
            if args['room_id'] is None:
                return "Error: Room ID is required", 400
            # check if room still has unpaid bills
            if check_total(args['room_id']) > 0:
                return "Error: Room has bill", 400
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
    @auth.login_required
    def put(self):
        try:
            args = guest_parser.parse_args()
            # check if new room is occupied
            if guest_collection.find_one({"_id": args['new_id']}) is not None:
                return "Error: Room occupied", 400
            # check if new room is under maintenance
            if check_room_status(args['new_id']) == False:
                return "Error: Room is under maintenance", 400
            # check if new room is the same as old room
            if args['room_id'] == args['new_id']:
                return "Error: Room is the same", 400            
            # check if old room is occupied
            if guest_collection.find_one({"_id": args['room_id']}) is None:
                return "Error: There are no guests to move", 400
            # move guest to a new room
            else:
                doc = guest_collection.find_one({"_id": args['room_id']})
                doc['_id'] = args['new_id']
                guest_collection.insert_one(doc)
                guest_collection.delete_one({"_id": args['room_id']})
                # update bill's room id
                bill_change_room(args['room_id'], args['new_id'])
                return "Guest moved to new room", 200
        except:
            return "Error updating guest information", 400         
    # ✔️
    # update guest information
    def patch(self):
        try:
            args = guest_parser.parse_args()
            # check if room is occupied
            if guest_collection.find_one({"_id": args['room_id']}) is None:
                return "Error: Room not occupied", 400
            else:
                doc = guest_collection.find_one({"_id": args['room_id']})
                check_null(args, doc)  
                guest_collection.update_one({"_id": args['room_id']}, {"$set": {"fname":args['fname'], "lname":args['lname'], 
                "email":args['email'], "checkin":args['checkin'], "checkout":args['checkout']}})
                return "Guest information updated", 200
        except:
            return "Error updating guest information", 400
 

def guest_total(room_id):
    guest_collection.update_one({"_id": room_id}, {"$set": {"total": check_total(room_id)}})
