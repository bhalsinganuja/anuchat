import pymongo
from flask import request
my_client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = my_client["chatapp"]
my_chat = mydb["all_chat"]
my_users = mydb["all_users"]

rooms = []
usernames = []
for x in my_chat.find({}, {"_id": 0,"room":1}):
    rooms.append(x['room'])
    print("rooms appended from database",x['room'])


for x in my_users.find({}, {"_id": 0,"user":1}):
    usernames.append(x['user'])
    print("usernames appended frm database",x['user'])


myquery = {'room': '4515123'}
mydoc = my_chat.find(myquery)
for z in mydoc:
    print(z['username']+":"+z['message'])

def newuser():
    room = request.args.get('room')



