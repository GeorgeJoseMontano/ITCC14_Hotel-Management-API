import random

string = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"

#create a key of 8 characters wit at least 1 number and 1 capital letter and 1 lowercase letter
def create_key():
    key = ""
    while len(key) < 8:
        key += random.choice(string)
    return key

#check if the key has at least 1 number and 1 capital letter and 1 lowercase letter
def check_key(key):
    if any(char.isdigit() for char in key) and any(char.isupper() for char in key) and any(char.islower() for char in key):
        return True
    else:
        return False

#generate a key that has at least 1 number and 1 capital letter and 1 lowercase letter
def generate_key():
    key = create_key()
    while check_key(key) == False:
        key = create_key()
    return key


