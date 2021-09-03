'use strict';

function joinToRoom(roomName){
    options1 = {
  appid: '75e50629d75d4fd59c9d5fc9c71c5a59',
  channel: roomName,
  uid: null
};

    var ws = 'ws://';
if(window.location.protocol=="https:"){ ws = 'wss://';}
var chatSocket = new WebSocket(ws + window.location.host + '/ws/chat/' + roomName + '/');
    $('#chat-list').hide()
    $('#join').show()
    $('#chat-window').show()
    $('#closeChatWindowButton').show()

chatSocket.onmessage = function(e) {
	var data = JSON.parse(e.data);
	if(user_id == data['user_id']){
	    $('#chat-log').append('<li style="padding-top: 0 !important; padding-bottom: 0 !important; width: 100%" class="p-2 chat-message-pov"></li>');
	    $('#chat-log').append('<li style="padding-top: 0 !important; padding-bottom: 0 !important" class="p-2 chat-message-pov"><a class="chat-message-time">'+data['time']+'</a><p class="chat-text-message-pov" >'+data['message']+'</p></li>');
	    $('#chat-log').append('<li style="padding-top: 16px !important; padding-bottom: 0 !important; width: 100%" class="p-2 chat-message-pov"></li>');

	}
	else{
	    $('#chat-log').append('<li style="padding-top: 0 !important; padding-bottom: 0 !important; width: 100%" class="p-2 chat-message-pov"></li>');
	    $('#chat-log').append('<li style="padding-top: 0 !important; padding-bottom: 0 !important" class="p-2 chat-message-pov-left"><p class="chat-text-message-pov" style="background: #E3E3E3; color: #333333">'+data['message']+'</p><a class="chat-message-time" style="margin-left: 10px">'+data['time']+'</a></li>');
	    $('#chat-log').append('<li style="padding-top: 16px !important; padding-bottom: 0 !important; width: 100%" class="p-2 chat-message-pov"></li>');
	}

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
	var Data = new Date();
    var Hour = Data.getHours();
    var Minutes = Data.getMinutes();
    var time = Hour+':'+Minutes
	if (message != '' && message != ' '){
        chatSocket.send(JSON.stringify({
            'message': message,
            'room': roomName,
            'time': time,
            'user_id': user_id
        }));
    }
	messageInputDom.value = '';
};
        $.ajax({
            url: "/ajax_load_messages/"+roomName,
            success: function (result) {
                var json = $.parseJSON(result);
                json.forEach(function(item, i, json) {
                    if (json[i].user_id == user_id){
                        $('#chat-log').append('<li class="p-2 chat-message-pov" style="padding-top: 0 !important; padding-bottom: 0 !important; width:100%"></li>'+
                                                '<li class="p-2 chat-message-pov" style="padding-top: 0 !important; padding-bottom: 0 !important">'+
                                                    '<a class="chat-message-time">'+json[i].time+'</a>'+
                                                    '<p class="chat-text-message-pov" >'+json[i].message+'</p>'+
                                                '</li>'+
                                                '<li class="p-2 chat-message-pov" style="padding-top: 16px !important; padding-bottom: 0 !important; width:100%"></li>')
                    }
                    else {
                        $('#chat-log').append('<li class="p-2 chat-message-pov" style="padding-top: 0 !important; padding-bottom: 0 !important; width:100%"></li>'+
                                                '<li class="p-2 chat-message-pov-left" style="padding-top: 0 !important; padding-bottom: 0 !important">'+
                                                    '<p class="chat-text-message-pov" style="background: #E3E3E3; color: #333333">'+json[i].message+'</p>'+
                                                    '<a class="chat-message-time" style="margin-left: 10px">'+json[i].time+'</a>'+
                                                '</li>'+
                                                '<li class="p-2 chat-message-pov" style="padding-top: 16px !important; padding-bottom: 0 !important; width:100%"></li>')
                    }
                })
            }
    })

}

$("#d1").show(function(){
    $("#chat-log").animate({ scrollTop: 100000 }, 50);


})

function closeChatWindow(){
    $('#chat-log').empty()
    $('#chat-list').show()
    $('#join').hide()
    $('#chat-window').hide()
    $('#closeChatWindowButton').hide()
    $('.teacher-name-p').empty()
}