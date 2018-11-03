from flask import Flask, request
from flask import render_template
from flask_socketio import SocketIO, send, emit, Namespace

app = Flask(__name__)
socketio = SocketIO(app)

app.config['SECRET_KEY'] = 'secret!'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['DEBUG'] = True

users = {}

@app.route("/")
def hello():
    return render_template('hello.html')

@app.route("/chat")
def chat():
    return render_template('chat.html')

@socketio.on('message_sent', "/chat")
def handle_message(message):
    print('MESSAGE RECEIVED')
    print(message)
    emit('message_received', {'message': message['message']}, broadcast=True)

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

    emit('contacted', user, room=recipient_sid)

if __name__ == '__main__':
    socketio.run(app)
