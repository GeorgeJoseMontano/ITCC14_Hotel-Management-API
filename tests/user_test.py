import requests

BASE = "http://127.0.0.1:5000/"

# Must return key
response = requests.post(BASE+"user/register", {"username":"test", "password":"test"})
print(response.json())

input()

# Must return user already exists
response = requests.post(BASE+"user/register", {"username":"test", "password":"test"})
print(response.json())

input()

# Must return key
response = requests.post(BASE+"user/login", {"username":"test", "password":"test"})
print(response.json())

input()

# Must return username does not exist
response = requests.post(BASE+"user/login", {"username":"ThisUserDoesNotExist", "password":"test"})
print(response.json())

input()

# Must return invalid password
response = requests.post(BASE+"user/login", {"username":"test", "password":"wrongPassword"})
print(response.json())

