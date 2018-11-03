var socket_chat = io.connect('http://' + document.domain + ':' + location.port + '/chat');

const textInput = document.querySelector('.text-input');
const chatContainer = document.querySelector('.chat-container');

function sendMessage(){
  socket_chat.emit('message_sent', {message: textInput.value});
  textInput.value = '';
}

socket_chat.on('message_received', function(i) {
  const messageDiv = document.createElement('p');
  const messageContent = document.createTextNode(i.message);
  console.log(i);
  messageDiv.className = 'message';
  messageDiv.appendChild(messageContent);
  chatContainer.appendChild(messageDiv);
});
