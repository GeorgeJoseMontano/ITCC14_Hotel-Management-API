import requests

BASE = "http://127.0.0.1:5000/"


room_id = input("Enter room id: ")

# Must return error room_id not found
response = requests.post(BASE+"guest", {"key":"978V9FBz", "fname":"George Jose", "lname":"Montano", 
"email":"email@email.com", "checkin":"2020-01-01", "checkout":"2020-01-02"})
print(response.json())
input()

# Must return success
response = requests.post(BASE+"guest", {"key":"978V9FBz", "room_id":room_id, "fname":"George Jose", "lname":"Montano", 
"email":"email@email.com", "checkin":"2020-01-01", "checkout":"2020-01-02"})
print(response.json())
input()

# Must return error room occupied
response = requests.post(BASE+"guest", {"key":"978V9FBz", "room_id":room_id, "fname":"George Jose", "lname":"Montano", 
"email":"email@email.com", "checkin":"2020-01-01", "checkout":"2020-01-02"})
print(response.json())
input()

# Must return error invalid key
response = requests.post(BASE+"guest", {"key":"wrongKey", "room_id":room_id, "fname":"George Jose", "lname":"Montano", 
"email":"email@email.com", "checkin":"2020-01-01", "checkout":"2020-01-02"})
print(response.json())
input()

response = requests.get(BASE+"guest?key=978V9FBz&room_id="+room_id)
print(response.json())
input()

response = requests.get(BASE+"guest?key=978V9FBz")
print(response.json())
input()


