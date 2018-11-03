let socket = io.connect('http://' + document.domain + ':' + location.port);
let private_socket = io.connect('http://' + document.domain + ':' + location.port + '/private');

const username = document.querySelector('.username');
const recipient = document.querySelector('.recipient');

function sendUsername() {
  private_socket.emit('username', username.value);
}

function startChat() {
  console.log("start");
  private_socket.emit("contact", recipient.value);
}

private_socket.on('contacted', function(sender){
  alert(sender + " wants to talk with you.");
});
