from flask_httpauth import HTTPBasicAuth
from connection import user_collection

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    if not (username and password):
        return False
    return user_collection.find_one({"username": username, "password": password})
    