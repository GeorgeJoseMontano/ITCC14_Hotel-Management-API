from parsers import bill_parser
from connection import guest_collection, bill_collection
from flask_restful import Resource
from checks import id_auto, check_total
from authorization import auth

class Bill(Resource):
    # ✔️
    @auth.login_required
    def post(self, room_id):
        try: 
            args = bill_parser.parse_args()
            # auto increment bill id
            bill_id = id_auto(bill_collection)
            # check if room is currently occupied
            if guest_collection.find_one({"_id": room_id}) is None:
                return "Error cannot add bill: Room not occupied", 400
            else:
                bill_collection.insert_one({"_id":bill_id, 'room_id':room_id, 'biller':args['biller'], 'amount':args['amount'], 'date':args['date']})
                return "New bill has been added successfully", 201
        except:
            return "There was an error adding the bill", 500
    # ✔️
    def get(self, room_id):
        try:
            get_info = bill_collection.find({"room_id": room_id})
            return [x for x in get_info], 200
        except:
            return "There was an error retrieving the bill", 500
    # ✔️
    @auth.login_required
    def delete(self, room_id):
        try:
            args = bill_parser.parse_args()
            # check if room is currently occupied
            if guest_collection.find_one({"_id": room_id}) is None:
                return "Error cannot delete bill: Room not occupied", 400
            # check if bill exists in database
            if bill_collection.find_one({"_id": args["bill_id"]}) is None:
                return "Error cannot delete bill: Bill does not exist", 400
            else:
                bill_collection.delete_one({"_id": args["bill_id"]})
                return "Bill payment was successful", 200
        except:
            return "There was an error deleting the bill", 500

    
    def initial_bill(self, room_id, amount, date):
        try:
            bill_id = id_auto(bill_collection)
            bill_collection.insert_one({"_id":bill_id,
            "room_id":room_id, 
            'biller':"room", 
            'amount':amount, 
            'date':date})
            return "Bill added", 201
        except:
            return "Error adding bill", 400

class Bill_Total(Resource):
    # ✔️
    def get(self):
        try:
            args = bill_parser.parse_args()
            room_id = args['room_id']
            # check if room is currently occupied
            if guest_collection.find_one({"_id": room_id}) is None:
                return "Error cannot get bill: Room not occupied", 400
            else:
                total = check_total(room_id)
                return total, 200
        except:
            return "There was an error retrieving the bill", 500
        

