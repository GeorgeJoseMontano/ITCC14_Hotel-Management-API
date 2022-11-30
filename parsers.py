from flask_restful import reqparse

guest_parser = reqparse.RequestParser()
guest_parser.add_argument("key", type=str, help="Key is required", required=False)
guest_parser.add_argument('new_id', type=int, help='Room assigned to guest', required=False)
guest_parser.add_argument('room_id', type=int, help='Room assigned to guest', required=False)
guest_parser.add_argument('fname', type=str, help='First name of the guest', required=False)
guest_parser.add_argument('lname', type=str, help='Last name of the guest', required=False)
guest_parser.add_argument('email', type=str, help='Email of the guest', required=False)
guest_parser.add_argument('checkin', type=str , help='Checkin date of the guest', required=False)
guest_parser.add_argument('checkout', type=str, help='Checkout date of the guest', required=False)

user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, help='Username of the user', required=True)
user_parser.add_argument('password', type=str, help='Password of the user', required=True)
user_parser.add_argument('new_password', type=str, help='New password of the user', required=False)

del_user_parser = reqparse.RequestParser()
del_user_parser.add_argument('key', type=str, help='Key of the user', required=False)
del_user_parser.add_argument('room_id', type=int, help='Room assigned to guest', required=False)