import requests

BASE = "http://127.0.0.1:5000/"

# response = requests.post(BASE+"guest", {"key":"0Q4ResKr", "room_id":153, "fname":"George Jose", "lname":"Montano", 
# "email":"email@email.com", "checkin":"2020-01-01", "checkout":"2020-01-02"})
# print(response.json())

# input()

response = requests.get(BASE+"bill/get/152")
print(response.json())

