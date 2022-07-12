import pymongo
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room
from database import get_user, user_info, get_password
from flask import Flask, render_template, redirect, request, session
from flask_session import Session

app = Flask(__name__)
socketio = SocketIO(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

my_client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = my_client["chatapp"]
my_rooms = mydb["all_rooms"]
my_users = mydb["all_users"]
my_chat = mydb['all_chat']
my_broadcastedmsgs = mydb["broadcastedmsgs"]


@app.route('/index',methods=['POST', 'GET'])
def home():
    if not session.get("name"):
        # if not there in the session then redirect to the login page
        return redirect("/login")

    return render_template("index.html")


rooms = []
usernames = []
for x in my_chat.find({}, {"_id": 0, "room": 1}):
    rooms.append(x['room'])

for x in my_users.find({}, {"_id": 0, "user": 1}):
    usernames.append(x['user'])


@app.route('/chat',methods=['POST', 'GET'])
def chat():
    print('inside chat function')
    username=session["name"]
    print(username)

    room = request.args.get('room')

    room_cnt = rooms.count(room)
    uname_cnt = usernames.count(session["name"])

    if room_cnt > 0 and uname_cnt > 0:
        return render_template('chat.html', username=session["name"], room=room)

    elif room_cnt == 0 and uname_cnt > 0:
        rooms.append(room)
        add_room_query = {"room": room}
        xk = my_rooms.insert_one(add_room_query)
        print("new room created:", xk)
        return render_template('chat.html', username=session["name"], room=room)

    elif uname_cnt == 0 and room_cnt > 0:
        usernames.append(session["name"])
        add_user_query = {"user": session["name"]}
        xk = my_users.insert_one(add_user_query)
        print("new user created:", xk)
        return render_template('chat.html', username=session["name"], room=room)
    elif uname_cnt == 0 and room_cnt == 0:
        # user_add
        usernames.append(session["name"])
        add_user_query = {"user": session["name"]}
        y = my_users.insert_one(add_user_query)
        print("new user created:", y)

        # room_add
        rooms.append(room)
        add_room_query = {"room": room}
        xk = my_rooms.insert_one(add_room_query)
        print("new room created:", xk)
        return render_template('chat.html', username=session["name"], room=room)
    else:
        print("inside else of chat function")
        return render_template("index.html")


@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data, room=data['room'])


@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info("{} has sent message to the room {}: {}".format(data['username'], data['room'], data['message']))

    # dev's code
    add_chat_query = {"room": data['room'], "username": data['username'], "message": data['message']}
    z = my_chat.insert_one(add_chat_query)
    print("new chat added:", z)

    socketio.emit('receive_message', data, room=data['room'])


@socketio.on('leave_room')
def handle_leave_room_event(data):
    app.logger.info("{} has left the room {}".format(data['username'], data['room']))
    leave_room(data['room'])
    socketio.emit('leave_room_announcement', data, room=data['room'])


@socketio.on('broadcasting')
def broadcasting(data):
    print("inside broadcasting or broad function")
    # dev's code
    add_chat_query = {"message": data}
    z = my_broadcastedmsgs.insert_one(add_chat_query)
    print("new msg broadcasted:", z)
    print("going to emit", data)
    data = "broadcasted msg:" + str(data)

    socketio.emit('rb', data)
    print("emitted broadcast")


# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     note = ''
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         if get_user(username) != None and get_password(password) != None:
#             return redirect(url_for('home'))
#         else:
#             note = 'username or password should be wrong'
#
#     return render_template('login.html', note=note)

@app.route('/')
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    messages = ''
    if request.method == 'POST':
        username = session["name"]
        password = request.form.get('password')

        if username == None:
            user_info(username, password)
            return redirect(url_for('login'))
        else:
            messages = 'Username already Exist'
            return redirect(url_for('login'))

    return render_template('signup.html', messages=messages)
fprevdata = []

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username=request.form.get('username')
        session["name"] = request.form.get("name")
        print(username)
        return render_template("index.html")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")

def msgshow(room):
    myquery = {'room': room}
    mydoc = my_chat.find(myquery)
    for z in mydoc:
        print(z['username']+":"+z['message'])
        data=str(z['username'])+":"+str(z['message'])
        print(data)

@socketio.on("prev_room_chat")
def prev_room_chat(data):
    print("previous chat: ", data)
    print("its datat-type", type(data))
    myquery={'room':data['room']}
    print("myquery",myquery)
    my_doc = my_chat.find(myquery, {"_id": 0})

    for z in my_doc:
        data = str("<b>" + z['username']) + "</b>" + ":" + str(z['message'])
        fprevdata.append(str(data) + "\n")

        print("data: ", data)
        conv = '<br>'.join([str(item) for item in fprevdata])
        print("final data: " + conv)

        socketio.emit("set_room_chat", conv)


print(fprevdata)

if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=8000)