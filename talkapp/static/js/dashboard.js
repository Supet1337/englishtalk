$('#dzModal').on('show.bs.modal', function (event) {
    var div = $(event.relatedTarget)
    var recipient = div.data('number')
    var emaill = div.data('email')
    var modal = $(this)
    $('#student_email').attr('href','mailto:'+emaill+'?subject=Домашнее задание&body=Привет, тебе пришло домашнее задание.')
})
function closeDoc(id){
    if ($("#docTab"+id).hasClass('active')){
        $("#home-tab").addClass('active');
        $("#home").addClass('show active');
    }
    $("#docLabel"+id).remove();
    $("#doc"+id).remove();
}

function closeVid(id,lid){
    if ($("#vidTab"+id).hasClass('active')){
        if(!$("#docTab"+lid).length){
            $("#home-tab").addClass('active');
            $("#home").addClass('show active');
        }
        else{
            $("#docTab"+lid).addClass('active');
            $("#doc"+lid).addClass('show active');
        }
    }
    $("#menu-toggle-right").show();
    $("#vidLabel"+id).remove();
    $("#vid"+id).remove();
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
                                 '<div class="card-header" id="doc-header'+id+'">'+
                                     '<a class="btn btn-white" style="border-radius: 0" id="buttonCollapseAudio'+id+'" data-toggle="collapse" href="#collapseAudio'+id+'" role="button" aria-expanded="false" aria-controls="collapseAudio'+id+'">'+
                                        'Аудиоматериалы'+
                                     '</a>'+
                                     '<a class="btn btn-white" style="border-radius: 0" id="buttonCollapseVideo'+id+'" data-toggle="collapse" href="#collapseVideo'+id+'" role="button" aria-expanded="false" aria-controls="collapseVideo'+id+'">'+
                                        'Видеоматериалы'+
                                     '</a>'+
                                 '</div>'+
                                 '<div class="collapse" id="collapseAudio'+id+'">'+
                                 '</div>'+
                                 '<div class="collapse" id="collapseVideo'+id+'">'+
                                 '</div>'+
                                 '<div class="card-body" style="height: 600px;">'+
                                 '<object><embed src="'+json[i].docx_url_copy+'" style="width: 100%; height: 100%"></object>'+
                                 '</div>'+
                                 '</div>');

                        if (is_teacher){
                            $("#doc"+id).append('<button type="button" class="btn btn-primary" data-toggle="modal" data-number="'+json[i].docx_url_copy+'" data-email="'+json[i].student_email+'" data-target="#dzModal">Отправить дз ученику</button>');
                            }

                        $.ajax({
                            url: "/ajax_load_lessons_audios/"+id,
                            success: function (result) {
                                var json = $.parseJSON(result);
                                json.forEach(function(item, i, json) {
                                    $("#collapseAudio"+id).append(
                                    '<p>'+json[i].audio_name+'</p>'+
                                    '<audio controls>'+
                                        '<source src="'+json[i].audio_url+'" type="audio/mpeg">'+
                                        '</audio>');
                                });
                        }}).then(
                        $.ajax({
                            url: "/ajax_load_lessons_videos/"+id,
                            success: function (result) {
                                var json = $.parseJSON(result);
                                json.forEach(function(item, i, json) {
                                    $("#collapseVideo"+id).append('<a id="openVid'+json[i].video_id+'" data-lesid="'+id+'" href="#">'+json[i].video_name+'</a>');
                                });

                        }}));
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

    $("#myTabContent").on('click','a[id^="openVid"]', function () {
        $("#menu-toggle-right").hide();
        i = $(this).attr("id");
        lid = $(this).data("lesid");
       const id = i.slice(7);
        $.ajax({
            url: "/ajax_load_video/"+id,
            success: function (result) {
                var json = $.parseJSON(result);
                json.forEach(function(item, i, json) {
                    if(!$("#vidLabel"+id).length){
                        $("#docTab"+lid).removeClass('active');
                        $("#doc"+lid).removeClass('show active');
                        $("#myTab").append('<li class="nav-item" id="vidLabel'+id+'" role="presentation">'+
                                 '<a class="nav-link active" id="vidTab'+id+'" data-toggle="tab" href="#vid'+id+'" role="tab" aria-controls="vid'+id+'" aria-selected="false">'+json[i].video_name+
                                 '<button type="button" class="close" onclick="closeVid('+id+','+lid+')" style="padding-left: 5px;" aria-label="Close">'+
                                 '<span aria-hidden="true">&times;</span>'+
                                 '</button>'+
                                 '</a>'+
                                 '</li>');
                        $("#myTabContent").append('<div class="tab-pane fade show active" id="vid'+id+'" role="tabpanel" aria-labelledby="vidTab'+id+'">'+
                                 '<div class="card-body" style="height: 480px;">'+
                                 '<video id="my-video" class="video-js mx-auto" controls preload="auto" width="720" height="480" poster="" data-setup="{}" >'+
                                 '<source src="'+json[i].video_url+'" type="video/mp4" />'+
                                 '</div>'+
                                 '</div>');
                    }

                    else {
                        $("#docTab"+lid).removeClass('active');
                        $("#doc"+lid).removeClass('show active');
                        $("#vidTab"+id).addClass('active');
                        $("#vid"+id).addClass('show active');
                    }
                });
        }});

    });
});



const domain = 'meet.jit.si';
const options = {
    roomName: room_name,
    width: '100%',
    height: 300,
    configOverwrite: {
        defaultLanguage: 'ru',
        enableClosePage: false,
        enableWelcomePage: false
    },
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
const api = new JitsiMeetExternalAPI(domain, options);


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
    $("#wrapper").toggleClass("left-toggled");
}

$(document).ready(function () {
 bsCustomFileInput.init()
})
function tog_right(){
    $("#angle-right").toggleClass("rotate");
    $("#wrapper").toggleClass("right-toggled");
}


$("#ddd8").click(function () {
    $("#dd8").toggleClass("active");
    $("#dd0").toggleClass("active");

})

$("#ddd1").click(function () {
    $("#dd1").toggleClass("active");
    $("#dd0").toggleClass("active");

})

$("#ddd3").click(function () {
    $("#dd3").toggleClass("active");
    $("#dd0").toggleClass("active");

})