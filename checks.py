from connection import guest_collection, user_collection, bill_collection, room_collection

# check if user key is valid
def check_key(key):
        if user_collection.find_one({"_id": key}) is not None:
            return True
        else:
            return False

# check if any fields are null
def check_parameters(args):
    if args['fname'] is None or args['lname'] is None or args['email'] is None or args['checkin'] is None or args['checkout'] is None or args['phone'] is None or args['num_guest'] is None:
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

def check_null_room(args, doc):
    if args['room_type'] is None:
        args['room_type'] = doc['room_type']
    if args['room_price'] is None:
        args['room_price'] = doc['room_price']
    if args['room_available'] is None:
        args['room_available'] = doc['room_available']
    if args['number_of_beds'] is None:
        args['number_of_beds'] = doc['number_of_beds']
    if args['mini_fridge'] is None:
        args['mini_fridge'] = doc['mini_fridge']
    if args['tv'] is None:
        args['tv'] = doc['tv']
    if args['ac'] is None:
        args['ac'] = doc['ac']
    if args['wifi'] is None:
        args['wifi'] = doc['wifi']
    if args['breakfast'] is None:
        args['breakfast'] = doc['breakfast']

def check_total (room_id):
    total = 0
    for x in bill_collection.find({"room_id": room_id}):
        total += x['amount']
    return total

# check room status if false    
def check_room_status(room_id):
    if room_collection.find_one({"_id": room_id})['room_available'] is False:
        return False
    else:
        return True 

# initial bill based on amount of room ID
def start_bill(room_id):
    room_bill = room_collection.find_one({"_id": room_id})['room_price']
    return room_bill

def bill_change_room(room_id, new_room_id):
    for x in bill_collection.find({"room_id": room_id}):
        bill_collection.update_one({"_id": x['_id']}, {"$set": {"room_id": new_room_id}})

def id_auto(collection):
    id = 1
    #check if id exists if not add 1 then check again
    while True:
        if collection.find_one({"_id": id}) is None:
            break
        else:
            id += 1
    return id