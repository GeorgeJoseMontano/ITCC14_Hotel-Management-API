from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

rooms = {
    'room1': {'guest_fname':'George Jose Montano'},
    'room2': {'guest_fname':'John Doe'},
}
class HelloWorld(Resource):
    def get(self):
        return jsonify({'hello': 'world'})

    def post(self):
        some_json = request.get_json()
        return jsonify({'you sent': some_json}), 201

class Guest(Resource):
    def get(self, room_id):
        return jsonify(rooms[room_id])

api. add_resource(HelloWorld, '/')
api. add_resource(Guest, '/guest/<string:room_id>')

if __name__ == '__main__':
    app.run(debug=True)

