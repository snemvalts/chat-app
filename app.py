from flask import Flask
from flask import render_template
from flask_socketio import SocketIO, send, emit



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

@socketio.on('message_sent')
def handle_message(message):
    print('MESSAGE RECEIVED')
    emit('message_received', {'data':'yooo'})

if __name__ == '__main__':
    socketio.run(app)
