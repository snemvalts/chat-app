from flask import Flask, request
from flask import render_template
from flask_socketio import SocketIO, send, emit, Namespace

import sqlite3


app = Flask(__name__)
socketio = SocketIO(app)

app.config['SECRET_KEY'] = 'secret!'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['DEBUG'] = True

users = {}
chat_pairs = {}

db = sqlite3.connect('app.db')


@app.route("/")
def hello():
    return render_template('app.html')

@socketio.on('message_sent')
def handle_message(message):
    cursor = db.cursor()
    for i in chat_pairs:
        if i == request.sid:
            recipient_sid = chat_pairs[i]
            break

        elif chat_pairs[i] == request.sid:
            recipient_sid = i
            break

    for name in users:
        if users.get(name) == request.sid:
            sender_name = name
        if users.get(name) == recipient_sid:
            recipient_name = name

    emit('message_received', {'message': message['message'], 'sender': sender_name}, room = recipient_sid)
    emit('message_received', {'message': message['message'], 'sender': sender_name}, room = request.sid)

    cursor.execute("INSERT INTO messages VALUES (?, ?, ?)", (sender_name, recipient_name, message['message']))
    db.commit()


@socketio.on('username', namespace="/private")
def receive_username(username):
    users[username] = request.sid
    print('CONNECTED: ' + username)
    print(users)

@socketio.on('contact', namespace="/private")
def user_connected(recipient):
    cursor = db.cursor()
    recipient_sid = users[recipient]

    for name in users:
        print(name)
        if users.get(name) == request.sid:
            print('found user')
            user = name

    chat_pairs[request.sid] = recipient_sid
    print("NEW CHAT PAIR!")
    print(chat_pairs)

    emit('contacted', user, room=recipient_sid)

    cursor.execute("SELECT * FROM messages WHERE (sender = ? AND recipient = ?) OR (recipient = ? AND sender = ?)", (user, recipient, recipient, user))

    for i in cursor:
        print(i, recipient_sid, request.sid)
        emit('message_received', {'message': i[2], 'sender': i[0]}, room = recipient_sid, namespace="")
        emit('message_received', {'message': i[2], 'sender': i[0]}, room = request.sid, namespace="")



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
