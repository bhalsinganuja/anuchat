import pymongo
from flask import Flask, render_template, redirect, request, session, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
socket = SocketIO(app)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["chatapp"]
my_col = mydb["chat"]

rooms = []
room_id=123



username="xyz"

@socket.on('add_room')
def add_room():
    username = request.args.get('username')
    room = request.args.get('room')

    def chatting():
        room_cnt = rooms.count(room)
        if room_cnt > 0:
            return render_template('chat.html')
        else:
            rooms.append(room)
            add_room_query = {"room": room_id}
            x = my_col.insert_one(add_room_query)
            print("new room created:", x)

            chatting()

    chatting()








