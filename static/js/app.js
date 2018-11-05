let socket = io.connect('http://' + document.domain + ':' + location.port);
let private_socket = io.connect('http://' + document.domain + ':' + location.port + '/private');

const textInput = document.querySelector('.text-input');
const chatContainer = document.querySelector('.chat-container');

function sendMessage(){
  console.log(textInput.value);
  socket.emit('message_sent', {message: textInput.value});
  textInput.value = '';
}

socket.on('message_received', function(i) {
  console.log(i);
  const messageDiv = document.createElement('p');
  const messageContent = document.createTextNode(i.sender + ": " + i.message);
  messageDiv.className = 'message';
  messageDiv.appendChild(messageContent);
  chatContainer.appendChild(messageDiv);
});


const username = document.querySelector('.username');
const recipient = document.querySelector('.recipient');

function sendUsername() {
  private_socket.emit('username', username.value);
}

function startChat() {
  private_socket.emit("contact", recipient.value);
}

private_socket.on('contacted', function(sender){
  alert("You are now talking with " + sender + ".");
});
