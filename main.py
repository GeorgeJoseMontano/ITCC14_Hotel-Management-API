from flask import Flask, send_from_directory
from flask_restful import Api
from resources import Guest_Public, Guest_Admin, User_Register, User_Login, User, Bill, Bill_Total, Rooms, Rooms_Admin
from flask_swagger_ui import get_swaggerui_blueprint


app = Flask(__name__)
api = Api(app)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Hotel Management System"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


api. add_resource(Guest_Public, '/guest/<int:room_id>')
api. add_resource(Guest_Admin, '/guest')
api. add_resource(User, '/user')
api. add_resource(User_Register, '/user/register')
api. add_resource(User_Login, '/user/login')
api. add_resource(Bill, '/bill/<int:room_id>')
api. add_resource(Bill_Total, '/bill/total')
api. add_resource(Rooms, '/room/<int:room_id>')
api. add_resource(Rooms_Admin, '/room')


if __name__ == '__main__':
    app.run(debug=True)