'use strict';


function getCookie(name) {

    var matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ))
    return matches ? decodeURIComponent(matches[1]) : undefined
}


function joinToRoom(roomName){
    options1 = {
    appid: '75e50629d75d4fd59c9d5fc9c71c5a59',
    channel: roomName,
    uid: null
};
$(".IDr").attr("id", roomName);
    var ws = 'ws://';
if(window.location.protocol=="https:"){ ws = 'wss://';}
var chatSocket = new ReconnectingWebSocket(ws + window.location.host + '/ws/chat/' + roomName + '/');
    $('#chat-list').hide()
    $('#join').show()
    $('#chat-window').show()
    $('#closeChatWindowButton').show()

chatSocket.onmessage = function(e) {

	var data = JSON.parse(e.data);
    if (data['is_file_message'] == true){
//	               console.log()
//                   $('#js-file').val("").fadeIn().delay(800)
//                   $('#chat-log').fadeOut(1000)
//                   $('#chat-log').html("")
//                   //$('#chat-log').load(document.URL +  ' #chat-log').fadeOut(1000, function(){chatSocket.refresh()});
//                   //$('#chat-log').fadeIn(1000)

setTimeout(() => {
               $.ajax({
                   url: "/ajax_load_url_file_messages/"+data['user_id']+'/'+roomName+'/'+data['time'].replace(/(^|\D)(\d)(?!\d)/g, '$10$2')+'/'+data['message'],
                   success: function (result) {
                       $('#chat-log').animate({ scrollTop: 100000 }, 50);
                       var json = $.parseJSON(result);
                           if(user_id == data['user_id']){
                                $('#chat-log').append('<li style="padding-top: 0 !important; padding-bottom: 0 !important; width: 100%" class="p-2 chat-message-pov"></li>');
                                $('#chat-log').append('<li style="padding-top: 0 !important; padding-bottom: 0 !important" class="p-2 chat-message-pov"><a class="chat-message-time">'+data['time']+'</a><a href download="'+json.file_message+'" ><p class="chat-text-message-pov" >'+data['message']+'</p></a></li>');
                                $('#chat-log').append('<li style="padding-top: 16px !important; padding-bottom: 0 !important; width: 100%" class="p-2 chat-message-pov"></li>');
                            }
                           else{
                               $('#chat-log').append('<li style="padding-top: 0 !important; padding-bottom: 0 !important; width: 100%" class="p-2 chat-message-pov"></li>');
                               $('#chat-log').append('<li style="padding-top: 0 !important; padding-bottom: 0 !important" class="p-2 chat-message-pov-left"><a href download="'+json.file_message+'" ><p class="chat-text-message-pov" style="background: #E3E3E3; color: #333333">'+data['message']+'</p></a><a class="chat-message-time" style="margin-left: 10px">'+data['time']+'</a></li>');
                               $('#chat-log').append('<li style="padding-top: 16px !important; padding-bottom: 0 !important; width: 100%" class="p-2 chat-message-pov"></li>');
                           }

                   }
               })},2000)

//	    $('#chat-log').append('<li style="padding-top: 0 !important; padding-bottom: 0 !important; width: 100%" class="p-2 chat-message-pov"></li>');
//	    $('#chat-log').append('<li style="padding-top: 0 !important; padding-bottom: 0 !important" class="p-2 chat-message-pov"><a class="chat-message-time">'+data['time']+'</a><a href download="/media/Messages/message_670/'+data['message']+'"><p class="chat-text-message-pov" >'+data['message']+'</p></a></li>');
//	    $('#chat-log').append('<li style="padding-top: 16px !important; padding-bottom: 0 !important; width: 100%" class="p-2 chat-message-pov"></li>');

}
    else{
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
    }
//	else{
//
//        if (data['is_file_message'] == true){
//           $('#js-file').val("").fadeIn().delay(800)
//           $('#chat-log').load(document.URL +  ' #chat-log').fadeOut(1000, function(){chatSocket.close();joinToRoom(roomName)});
//           $('#chat-log').fadeIn(1000)
//        }
//	    $('#chat-log').append('<li style="padding-top: 0 !important; padding-bottom: 0 !important; width: 100%" class="p-2 chat-message-pov"></li>');
//	    $('#chat-log').append('<li style="padding-top: 0 !important; padding-bottom: 0 !important" class="p-2 chat-message-pov-left"><p class="chat-text-message-pov" style="background: #E3E3E3; color: #333333">'+data['message']+'</p><a class="chat-message-time" style="margin-left: 10px">'+data['time']+'</a></li>');
//	    $('#chat-log').append('<li style="padding-top: 16px !important; padding-bottom: 0 !important; width: 100%" class="p-2 chat-message-pov"></li>');
	$('#chat-log').animate({ scrollTop: 100000 }, 50);
	}
        $('#chat-log').animate({ scrollTop: 100000 }, 50);

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
    var time = (Hour+':'+Minutes).replace(/(^|\D)(\d)(?!\d)/g, '$10$2')
	if (message.trim() != ''){
        chatSocket.send(JSON.stringify({
            'message': message,
            'room': roomName,
            'time': time,
            'user_id': user_id,
            'is_file_message': false
        }));
    }
	messageInputDom.value = '';
};

$("#js-file").change(function(){

    var crsid = $(".ID").attr("id");
    var roomid = $(".IDr").attr("id");
    var formData = new FormData();
    formData.append('file', $("#js-file")[0].files[0]);
    var message = $("#js-file")[0].files[0].name;

	var Data = new Date();
    var Hour = Data.getHours();
    var Minutes = Data.getMinutes();
    var time = Hour+':'+Minutes
    var datetime = (time+':'+Data.getSeconds()).replace(/(^|\D)(\d)(?!\d)/g, '$10$2');
	if (message.trim() != ''){
        chatSocket.send(JSON.stringify({
            'message': message,
            'room': roomName,
            'time': time,
            'user_id': user_id,
            'is_file_message': true
        }));
    }setTimeout(() => {
    		$.ajax({
    			type: "POST",
    			url: '/message-file-upload/'+datetime+'/'+message+'/'+crsid+'/'+window.location.href.split('/').pop(),
    			cache: false,
    			contentType: false,
    			processData: false,
    			data: formData,
    			headers:{
                    "X-CSRFToken": getCookie('csrftoken')
                },
                success: function(data) {
                    $('#js-file').val("")
                    //$('#chat-log').load(document.URL +  ' #chat-log').fadeOut(1000, function(){chatSocket.close();joinToRoom(roomName); chatSocket.send('ok')});
                    //$('#chat-log').load(document.URL +  ' #chat-log').fadeOut(1000, function(){chatSocket.refresh();joinToRoom(roomName)});
                    //chatSocket.refresh()
                    //$('#chat-log').fadeIn(1000)
                    //elementUpdate('#chat-log')
                },
                 error: function(xhr, textStatus, error){
                      console.log(xhr.statusText);
                      console.log(textStatus);
                      console.log(error);
                  }
    		})}, 100);

	//messageInputDom.value = '';

});

        $.ajax({
            url: "/ajax_load_messages/"+roomName,
            success: function (result) {
                $('#chat-log').animate({ scrollTop: 100000 }, 50);
                var json = $.parseJSON(result);
                json.forEach(function(item, i, json) {
                    if (json[i].user_id == user_id){
                        if (json[i].message_url != ""){
                            $('#chat-log').append('<li class="p-2 chat-message-pov" style="padding-top: 0 !important; padding-bottom: 0 !important; width:100%"></li>'+
                                                    '<li class="p-2 chat-message-pov" style="padding-top: 0 !important; padding-bottom: 0 !important">'+
                                                        '<a class="chat-message-time">'+json[i].time.replace(/(^|\D)(\d)(?!\d)/g, '$10$2')+'</a>'+
                                                        '<a href="" download="'+json[i].message_url+'" ><p class="chat-text-message-pov" >'+json[i].message+'</p></a>'+
                                                    '</li>'+
                                                    '<li class="p-2 chat-message-pov" style="padding-top: 16px !important; padding-bottom: 0 !important; width:100%"></li>')

                        }
                        else{
                            $('#chat-log').append('<li class="p-2 chat-message-pov" style="padding-top: 0 !important; padding-bottom: 0 !important; width:100%"></li>'+
                                                    '<li class="p-2 chat-message-pov" style="padding-top: 0 !important; padding-bottom: 0 !important">'+
                                                        '<a class="chat-message-time">'+json[i].time.replace(/(^|\D)(\d)(?!\d)/g, '$10$2')+'</a>'+
                                                        '<p class="chat-text-message-pov" >'+json[i].message+'</p>'+
                                                    '</li>'+
                                                    '<li class="p-2 chat-message-pov" style="padding-top: 16px !important; padding-bottom: 0 !important; width:100%"></li>')
                        }

                    }
                    else {
                         if (json[i].message_url != "" ){
                             $('#chat-log').append('<li class="p-2 chat-message-pov" style="padding-top: 0 !important; padding-bottom: 0 !important; width:100%"></li>'+
                                                     '<li class="p-2 chat-message-pov-left" style="padding-top: 0 !important; padding-bottom: 0 !important">'+
                                                         '<a href="" download="'+json[i].message_url+'" ><p class="chat-text-message-pov" style="background: #E3E3E3; color: #333333">'+json[i].message+'</p></a>'+
                                                         '<a class="chat-message-time" style="margin-left: 10px">'+json[i].time.replace(/(^|\D)(\d)(?!\d)/g, '$10$2')+'</a>'+
                                                     '</li>'+
                                                     '<li class="p-2 chat-message-pov" style="padding-top: 16px !important; padding-bottom: 0 !important; width:100%"></li>')
                         }
                         else{
                             $('#chat-log').append('<li class="p-2 chat-message-pov" style="padding-top: 0 !important; padding-bottom: 0 !important; width:100%"></li>'+
                                                     '<li class="p-2 chat-message-pov-left" style="padding-top: 0 !important; padding-bottom: 0 !important">'+
                                                         '<p class="chat-text-message-pov" style="background: #E3E3E3; color: #333333">'+json[i].message+'</p>'+
                                                         '<a class="chat-message-time" style="margin-left: 10px">'+json[i].time.replace(/(^|\D)(\d)(?!\d)/g, '$10$2')+'</a>'+
                                                     '</li>'+
                                                     '<li class="p-2 chat-message-pov" style="padding-top: 16px !important; padding-bottom: 0 !important; width:100%"></li>')

                         }


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