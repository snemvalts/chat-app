from flask import Flask, request
from flask import render_template
from flask_socketio import SocketIO, send, emit, Namespace

app = Flask(__name__)
socketio = SocketIO(app)

app.config['SECRET_KEY'] = 'secret!'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['DEBUG'] = True

users = {}
chat_pairs = {}

@app.route("/")
def hello():
    return render_template('app.html')

@socketio.on('message_sent')
def handle_message(message):
    for i in chat_pairs:
        if i == request.sid:
            recipient_sid = chat_pairs[i]
            break

        elif chat_pairs[i] == request.sid:
            recipient_sid = i
            break

    for name in users:
        if users.get(name) == request.sid:
            user = name

    emit('message_received', {'message': message['message'], 'sender': user}, room = recipient_sid)
    emit('message_received', {'message': message['message'], 'sender': user}, room = request.sid)

@socketio.on('username', namespace="/private")
def receive_username(username):
    users[username] = request.sid
    print('CONNECTED: ' + username)
    print(users)

@socketio.on('contact', namespace="/private")
def user_connected(recipient):
    recipient_sid = users[recipient]

    for name in users:
        if users.get(name) == request.sid:
            user = name

    chat_pairs[request.sid] = recipient_sid
    print("NEW CHAT PAIR!")
    print(chat_pairs)

    emit('contacted', user, room=recipient_sid)

if __name__ == '__main__':
    socketio.run(app)
