import requests

BASE = "http://127.0.0.1:5000/"

# Must return room not occupied
response = requests.get(BASE+"guest/120", {"key":"uhQd0Tj1"})
print(response.json())

input()

# Must return success
response = requests.get(BASE+"guest/121", {"key":"uhQd0Tj1"})
print(response.json())

input()


# Must return invalid key
response = requests.delete(BASE+"guest/121?key=wrongKey")
print(response.json())

input()

# Must return room unoccupied

response = requests.delete(BASE+"guest/120?key=uhQd0Tj1")
print(response.json())

input()

# Must return success
response = requests.delete(BASE+"guest/121?key=uhQd0Tj1")
print(response.json())

input()

# Must return success
response = requests.post(BASE+"guest/120", {"key":"uhQd0Tj1", "fname":"George Jose", "lname":"Montano", 
"email":"email@email.com", "checkin":"2020-01-01", "checkout":"2020-01-02"})
print(response.json())

input()

# Must return room occupied error
response = requests.post(BASE+"guest/120", {"key":"uhQd0Tj1", "fname":"George Jose", "lname":"Montano", 
"email":"email@email.com", "checkin":"2020-01-01", "checkout":"2020-01-02"})
print(response.json())

input()

# Must return invalid key error
response = requests.post(BASE+"guest/10020", {"key":"wrongKey", "fname":"George Jose", "lname":"Montano", 
"email":"email@email.com", "checkin":"2020-01-01", "checkout":"2020-01-02"})
print(response.json())

input()

# Must return guest information updated
response = requests.put(BASE+"guest/120", {"key":"uhQd0Tj1", "fname":"George", "lname":"Padilla", 
"email":"email@email.com", "checkin":"2020-01-01", "checkout":"2020-01-02"})
print(response.json())

input()

# Must return guest moved to new room
response = requests.put(BASE+"guest/120", {"key":"uhQd0Tj1", "fname":"George", "lname":"Padilla", 
"email":"email@email.com", "checkin":"2020-01-01", "checkout":"2020-01-02", "room_id":121})
print(response.json())

input()

# Must return guest invalid key error
response = requests.put(BASE+"guest/121", {"key":"wrongKey", "fname":"George", "lname":"Padilla", 
"email":"email@email.com", "checkin":"2020-01-01", "checkout":"2020-01-02", "room_id":121})
print(response.json())

input()

# Must return room unoccupied
response = requests.put(BASE+"guest/120", {"key":"uhQd0Tj1", "fname":"George", "lname":"Padilla", 
"email":"email@email.com", "checkin":"2020-01-01", "checkout":"2020-01-02", "room_id":121})
print(response.json())

input()







{
    "key":"dT9owhSG",
    "room_id":129,
    "biller":"water",
    "amount":100
}