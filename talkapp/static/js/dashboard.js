$('#dzModal').on('show.bs.modal', function (event) {
    var div = $(event.relatedTarget)
    var recipient = div.data('number')
    var modal = $(this)
    modal.find('.modal-title').text(recipient)
    $('#dzFile').attr('href',recipient)
})
function closeDoc(id){
    $("#docLabel"+id).remove();
    $("#doc"+id).remove();
    $("#home-tab").addClass('active');
    $("#home").addClass('show active');
}


$(document).ready(function(){
    $('a[id^="openDoc"]').click(function () {
        i = $(this).attr("id");
       const id = i.slice(7);
        $.ajax({
            url: "/ajax_load_lessons/"+id,
            success: function (result) {
                var json = $.parseJSON(result);
                json.forEach(function(item, i, json) {
                    if(!$("#docLabel"+id).length){
                        $("#home-tab").removeClass('active');
                        $("#home").removeClass('show active');
                        $("#myTab").append('<li class="nav-item" id="docLabel'+id+'" role="presentation">'+
                                 '<a class="nav-link active" id="docTab'+id+'" data-toggle="tab" href="#doc'+id+'" role="tab" aria-controls="doc'+id+'" aria-selected="false">'+json[i].name+
                                 '<button type="button" class="close" onclick="closeDoc('+id+')" style="padding-left: 5px;" aria-label="Close">'+
                                 '<span aria-hidden="true">&times;</span>'+
                                 '</button>'+
                                 '</a>'+
                                 '</li>');
                        $("#myTabContent").append('<div class="tab-pane fade show active" id="doc'+id+'" role="tabpanel" aria-labelledby="docTab'+id+'">'+
                                 '<div class="card-body" style="height: 700px;">'+
                                 '<object><embed src="'+json[i].docx_url+'" style="width: 100%; height: 100%"></object>'+
                                 '</div>'+
                                 '</div>');

                        $.ajax({
                            url: "/ajax_load_lessons_videos/"+id,
                            success: function (result) {
                                $("#doc"+id).append('<p>Видеоматериалы:</p>');
                                var json = $.parseJSON(result);
                                json.forEach(function(item, i, json) {
                                    $("#doc"+id).append('<video id="my-video" class="video-js"controls preload="auto" width="640" height="264" poster="" data-setup="{}" >'+
                                     '<source src="'+json[i].video_url+'" type="video/mp4" />'
                                    );
                                });

                        }})
                        $.ajax({
                            url: "/ajax_load_lessons_audios/"+id,
                            success: function (result) {
                                $("#doc"+id).append('<p>Аудиоматериалы:</p>');
                                var json = $.parseJSON(result);
                                json.forEach(function(item, i, json) {
                                    $("#doc"+id).append('<audio controls>'+
                                        '<source src="'+json[i].audio_url+'" type="audio/mpeg">'+
                                        '</audio>');
                                });
                        }})
                    }

                    else {
                        $("#home-tab").removeClass('active');
                        $("#home").removeClass('show active');
                        $("#docTab"+id).addClass('active');
                        $("#doc"+id).addClass('show active');
                    }
                });
        }});

    });
})
const domain = 'meet.jit.si';
const options = {
    roomName: 'asdffhdgfha',
    width: '100%',
    height: 700,
    configOverwrite: { defaultLanguage: 'ru',
     enableClosePage: false},
    interfaceConfigOverwrite: {
        APP_NAME : "English-talk meet",
        DEFAULT_REMOTE_DISPLAY_NAME : 'Ученик',
        DEFAULT_LOCAL_DISPLAY_NAME : "Я",
        JITSI_WATERMARK_LINK : "",
        NATIVE_APP_NAME : "English-talk meet",
        HIDE_KICK_BUTTON_FOR_GUESTS: true,
        MOBILE_DOWNLOAD_LINK_ANDROID: '',
        MOBILE_DOWNLOAD_LINK_IOS: '',
     },
    parentNode: document.querySelector('#chat')
};
//const api = new JitsiMeetExternalAPI(domain, options);


$(document).ready(function(){
    $('button[id^="c"]').focus(function () {
	    elementClick = $(this).attr("id");
	    $("#"+elementClick).addClass("animate__animated animate__heartBeat");
		return false;
	});
});

var s = 1;
function tog(){
    if(s % 2 == 1)
        document.getElementById("angle").className = "fa fa-angle-right";
    else
        document.getElementById("angle").className = "fa fa-angle-left";
    s += 1;
    $("#wrapper").toggleClass("toggled");
}

$(document).ready(function () {
 bsCustomFileInput.init()
})
