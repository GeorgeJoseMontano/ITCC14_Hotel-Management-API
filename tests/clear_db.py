import requests

BASE = "http://127.0.0.1:5000/"

# Must return success
response = requests.delete(BASE+"guest")

print(response.json())