from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
mydb = client['chatapp']
mycollection = mydb['Signup']

my_data = mydb['signup']


def user_info(username, password):
    my_data.insert_one({"username": username, "password": password})


def save_user(name, room, message):
    mycollection.insert_one({"name": name, "room": room, "message":message})


def get_user(username1):
    x = my_data.find_one({"username": username1})
    return x


def get_password(password):
    y = my_data.find_one({"password": password})
    return y