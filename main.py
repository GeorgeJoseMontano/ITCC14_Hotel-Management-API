from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('fname', type=str, help='First name of the guest')
parser.add_argument('room_id', type=int, help='Room ID of the guest')


rooms = {
    101: {'fname':'George Jose', "guest_lname":"Montano", "room_id":101},
    102: {'fname':'John Doe'},
}

class Guest(Resource):
    def get(self, room_id):
        return jsonify(rooms[room_id])
    
    def put(self, room_id):
        args = parser.parse_args()
        fname = {'fname': args['fname']}
        rooms[room_id] = args
        return rooms[room_id], 201

    def delete(self, room_id):
        del rooms[room_id]
        return jsonify(rooms)

class Guest_Base(Resource):
    def get(self):
        return rooms

api. add_resource(Guest_Base, '/guest/')
api. add_resource(Guest, '/guest/<int:room_id>')

if __name__ == '__main__':
    app.run(debug=True)

