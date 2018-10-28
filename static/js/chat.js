let socket = io.connect('http://' + document.domain + ':' + location.port);

function sendMessage(){
  socket.emit('message_sent', {data: 'yoo dude'});
}

socket.on('message_received', function(i) {
  alert('received from server:'+ i.data);
});