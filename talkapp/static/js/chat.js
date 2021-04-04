'use strict';

// var roomName = {{ room_name_json }};
var roomName = room;


$("#d1").show(function(){
    $("#chat-log").animate({ scrollTop: 100000 }, 50);
    console.log("sssssssssss")

})

var ws = 'ws://';
if(window.location.protocol=="https:"){ ws = 'wss://';}
var chatSocket = new WebSocket(ws + window.location.host + '/ws/chat/' + roomName + '/');

chatSocket.onmessage = function(e) {
	var data = JSON.parse(e.data);
	// var message = data['message'];
	// document.querySelector('#chat-log').value += (message + '\n');
	// document.querySelector('#chat-log').append('<li>'+message+'</li>');
	$('#chat-log').append('<li class="p-2"><span>'+data['user']+'</span> '+data['message']+'</li>');
	$('#chat-log').animate({ scrollTop: 100000 }, 50);
};

chatSocket.onclose = function(e) {
	console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
	if (e.keyCode === 13) {  // enter, return
		document.querySelector('#chat-message-submit').click();
	}
};

document.querySelector('#chat-message-submit').onclick = function(e) {
	var messageInputDom = document.querySelector('#chat-message-input');
	var message = messageInputDom.value;
	if (message != '' && message != ' '){
        chatSocket.send(JSON.stringify({
            'message': message,
            'room': room,
        }));
    }
	messageInputDom.value = '';
};