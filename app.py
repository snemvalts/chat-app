from flask import Flask, request
from flask import render_template
from flask_socketio import SocketIO, send, emit, Namespace

app = Flask(__name__)
socketio = SocketIO(app)

app.config['SECRET_KEY'] = 'secret!'
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/")
def hello():
    return render_template('hello.html')

@app.route("/chat/")
def chat():
    return render_template('chat.html')

@socketio.on('connected')
def connected(i):
    print('CONNECTED:')
    print(request.sid)
    print(i)

@socketio.on('message_sent')
def handle_message(message):
    print('MESSAGE RECEIVED')
    print(message)
    emit('message_received', {'message': message['message']}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)
