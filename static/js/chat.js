let socket = io.connect('http://' + document.domain + ':' + location.port);
const textInput = document.querySelector('.text-input');
const chatContainer = document.querySelector('.chat-container');
function sendMessage(){
  socket.emit('message_sent', {message: textInput.value});
  textInput.value = '';
}

socket.on('message_received', function(i) {
  const messageDiv = document.createElement('p');
  const messageContent = document.createTextNode(i.message);
  console.log(i);
  messageDiv.className = 'message';
  messageDiv.appendChild(messageContent);
  chatContainer.appendChild(messageDiv);
});
