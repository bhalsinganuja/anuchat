
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO
from database import get_user, user_info, get_password

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/login', methods=['POST', 'GET'])
def login():
    note = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if get_user(username)!= None and get_password(password) != None:
            return redirect(url_for('home'))
        else:
            note = 'username or password should be wrong'
            #return render_template('login.html', note=note)

    return render_template('login.html', note=note)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    messages = ''
    if request.method == 'POST':
        username1 = request.form.get('username')
        password = request.form.get('password')
        #x = get_user(username1)
        if get_user(username1)==None:
            user_info(username1, password)
            return redirect(url_for('login'))
        else:
            messages = 'user already exist'
    return render_template('signup.html', messages=messages)








