$('#dzModal').on('show.bs.modal', function (event) {
    var div = $(event.relatedTarget)
    var recipient = div.data('number')
    var emaill = div.data('email')
    var modal = $(this)
    $('#student_email').attr('href','mailto:'+emaill+'?subject=Домашнее задание&body=Привет, тебе пришло домашнее задание.')
})
function closeDoc(id){
    if ($("#docTab"+id).hasClass('nvlnk-act')){
        $("#home-tab").addClass('active');
        $("#home").addClass('show active');
    }
    $("#bread-item"+id).remove();
    $(".breadcrumb-item").last().addClass('active');
    $("#buttonCollapseAudio"+id).remove();
    $("#buttonCollapseVideo"+id).remove();
    $("#docLabel"+id).remove();
    $("#doc"+id).remove();
}

function closeVid(id,lid){
    $("#buttonCollapseVideo"+lid).addClass('nvlnk-act');
    $("#doc"+lid).addClass('show active');
    $("#bread-vid"+id).remove();
    $(".breadcrumb-item").last().addClass('active');
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
                        $("#home-tab").removeClass('nvlnk-act');
                        $("#home").removeClass('show active');
                        $("#myTab").append(
                                    '<li class="nav-item mb-1" role="presentation">'+
                                         '<a class="nvlnk " id="buttonCollapseAudio'+id+'" data-toggle="collapse" href="#" onclick="showAudios('+id+')" role="button" aria-expanded="false" aria-controls="collapseAudio'+id+'">'+'Аудио'+
                                    '</li>'+

                                    '<li class="nav-item mb-1" role="presentation">'+
                                        '<a class="nvlnk " id="buttonCollapseVideo'+id+'" data-toggle="collapse" href="#" onclick="showVideos('+id+')" role="button" aria-expanded="false" aria-controls="collapseVideo'+id+'">'+'Видео'+
                                    '</li>'+

                                 '<li  class="nav-item mb-1 mr-1" id="docLabel'+id+'" role="presentation">'+
                                 '<a class="nvlnk nvlnk-act" id="docTab'+id+'" onclick="docClick('+id+')" data-toggle="tab" href="#doc'+id+'" role="tab" aria-controls="doc'+id+'" aria-selected="false">'+json[i].name+
                                 '<button type="button" class="close" id="docClose'+id+'" onclick="closeDoc('+id+')" style="padding-left: 5px;" aria-label="Close">'+
                                 '<span aria-hidden="true">&times;</span>'+
                                 '</button>'+
                                 '</a>'+
                                 '</li>');
                        $("#myTabContent").append('<div class="tab-pane fade show active" id="doc'+id+'" role="tabpanel" aria-labelledby="docTab'+id+'">'+
                                 //'<div class="card-header" id="doc-header'+id+'">'+
                                    // '<a class="btn btn-white" style="border-radius: 0" id="buttonCollapseAudio'+id+'" data-toggle="collapse" href="#collapseAudio'+id+'" role="button" aria-expanded="false" aria-controls="collapseAudio'+id+'">'+
                                     //   'Аудиоматериалы'+
                                    // '</a>'+
                                    // '<a class="btn btn-white" style="border-radius: 0" id="buttonCollapseVideo'+id+'" data-toggle="collapse" href="#collapseVideo'+id+'" role="button" aria-expanded="false" aria-controls="collapseVideo'+id+'">'+
                                    //    'Видеоматериалы'+
                                    // '</a>'+
                                 //'</div>'+
                                 '<div class="collapse" id="collapseAudio'+id+'">'+
                                 '</div>'+
                                 '<div class="collapse" id="collapseVideo'+id+'">'+
                                 '</div>'+
                                 '<div class="collapse show" id="docCard'+id+'" style="height: 600px;">'+
                                 '<object><embed src="'+json[i].docx_url_copy+'" style="width: 100%; height: 100%"></object>'+
                                 '</div>'+
                                 '</div>');
                        $(".breadcrumb-item").removeClass('active');
                        $("#breadcrumb").append('<li class="breadcrumb-item active" id="bread-item'+id+'">'+json[i].name+'</li>');

                        $.ajax({
                            url: "/ajax_load_lessons_audios/"+id,
                            success: function (result) {
                                var json = $.parseJSON(result);
                                json.forEach(function(item, i, json) {
                                    $("#collapseAudio"+id).append(
                                    '<p style="padding-top: 20px; margin-bottom: 14px">'+json[i].audio_name+'</p>'+
                                    '<div id="audioPlayer'+json[i].audio_id+'"></div>'
                                    );
                                    var audioPlayer = new Playerjs({id:"audioPlayer"+json[i].audio_id, file:json[i].audio_url, player: 2});
                                });
                        }}).then(
                        $.ajax({
                            url: "/ajax_load_lessons_videos/"+id,
                            success: function (result) {
                                var json = $.parseJSON(result);
                                json.forEach(function(item, i, json) {
                                    $("#collapseVideo"+id).append(
                                        '<div class="row">'+
                                          '<div class="col" id="openVid'+json[i].video_id+'" style="display: flex; cursor: pointer; padding-top: 40px" data-lesid="'+id+'">'+
                                              '<div id="player'+json[i].video_id+'" style="width: 160px; height: 100px; border-radius: 50px"></div>'+
                                              '<div style="margin-left: 12px; margin-top: 24px">'+
                                                  '<a style="font-family: Arial;font-style: normal;font-weight: bold;font-size: 16px;line-height: 18px;color: #333333; margin-bottom: 0" class="video-name" href="#">'+json[i].video_name+'</a>'+
                                                  '<p style="font-family: Arial;font-style: normal;font-weight: bold;font-size: 12px;line-height: 14px;color: #828282;">14:03 мин</p>'+
                                              '</div>'+
                                          '</div>'+
                                      '</div>'
                                    );
                                    var player = new Playerjs({id:"player"+json[i].video_id, file:json[i].video_url, player: 1});
                                });

                        }}));
                    }

                    else {
                        $("#home-tab").removeClass('nvlnk-act');
                        $("#home").removeClass('show active');
                        $("#docTab"+id).addClass('nvlnk-act');
                        $("#doc"+id).addClass('show active');
                    }
                });
        }});

    });

    $("#myTabContent").on('click','div[id^="openVid"]', function () {
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
                        $("#buttonCollapseVideo"+lid).removeClass('nvlnk-act');
                        $("#doc"+lid).removeClass('show active');
                        $("#myTab").append('<li class="nav-item" id="vidLabel'+id+'" role="presentation">'+
                                 '<a class="nvlnk nvlnk-act vidosikTab" id="vidTab'+id+'" onclick="videoOpen('+id+','+lid+')" data-toggle="tab" href="#vid'+id+'" role="tab" aria-controls="vid'+id+'" aria-selected="false">'+json[i].video_name+
                                 '<button type="button" class="close vidClose" onclick="event.stopPropagation();closeVid('+id+','+lid+');" style="padding-left: 5px;" aria-label="Close">'+
                                 '<span aria-hidden="true">&times;</span>'+
                                 '</button>'+
                                 '</a>'+
                                 '</li>');
                        $("#myTabContent").append('<div class="tab-pane fade show active vidosik" id="vid'+id+'" role="tabpanel" aria-labelledby="vidTab'+id+'">'+
                                 '<div class="card-body" style="height: 480px; padding-top: 0">'+
                                 '<div class="mx-auto" id="bgPlayer'+json[i].video_id+'" style="width: 90%; height: 440px;"></div>'+
                                 '</div>'+
                                 '</div>');
                        var player = new Playerjs({id:"bgPlayer"+json[i].video_id, file:json[i].video_url, player: 1});
                    }

                    else {
                        $("#docTab"+lid).removeClass('nvlnk-act');
                        $("#doc"+lid).removeClass('show active');
                        $("#vidTab"+id).addClass('nvlnk-act');
                        $("#vid"+id).addClass('show active');
                    }
                $(".breadcrumb-item").removeClass('active');
                $("#breadcrumb").append('<li class="breadcrumb-item active" id="bread-vid'+id+'">'+json[i].video_name+'</li>');
                });
        }});

    });
});






$(document).ready(function(){
    $('button[id^="c"]').focus(function () {
	    elementClick = $(this).attr("id");
	    $("#"+elementClick).addClass("animate__animated animate__heartBeat");
		return false;
	});
});

function showVideos(id){
    if(!$('#buttonCollapseVideo'+id).hasClass('nvlnk-act')){
        $('#docCard'+id).removeClass('show');
        $('#collapseVideo'+id).toggleClass('show');
        $('#buttonCollapseVideo'+id).toggleClass('nvlnk-act');
        $('#docTab'+id).removeClass('nvlnk-act');
        $('#collapseAudio'+id).removeClass('show');
        $('#buttonCollapseAudio'+id).removeClass('nvlnk-act');
        $('#docClose'+id).hide();
        $("#doc"+id).addClass('show active');
        $('.vidClose').hide();
        $('.vidosik').removeClass('show active');
        $('.vidosikTab').removeClass('nvlnk-act');
    }
}

function showAudios(id){
    if(!$('#buttonCollapseAudio'+id).hasClass('nvlnk-act')){
        $('#docCard'+id).removeClass('show');
        $('#collapseAudio'+id).toggleClass('show');
        $('#buttonCollapseAudio'+id).toggleClass('nvlnk-act');
        $('#docTab'+id).removeClass('nvlnk-act');
        $('#collapseVideo'+id).removeClass('show');
        $('#buttonCollapseVideo'+id).removeClass('nvlnk-act');
        $('#docClose'+id).hide();
        $("#doc"+id).addClass('show active');
        $('.vidClose').hide();
        $('.vidosik').removeClass('show active');
        $('.vidosikTab').removeClass('nvlnk-act');
    }
}

function docClick(id){
    if(!$('#docTab'+id).hasClass('nvlnk-act')){
        $('#docCard'+id).toggleClass('show');
        $('#collapseAudio'+id).removeClass('show');
        $('#buttonCollapseAudio'+id).removeClass('nvlnk-act');
        $('#docTab'+id).toggleClass('nvlnk-act');
        $('#collapseVideo'+id).removeClass('show');
        $('#buttonCollapseVideo'+id).removeClass('nvlnk-act');
        $('#docClose'+id).show();
        $('.vidosik').removeClass('show active');
        $('.vidosikTab').removeClass('nvlnk-act');
        $("#doc"+id).addClass('show active');
        $('.vidClose').hide();
    }
}

function videoOpen(id, lid){
    if(!$('#vidTab'+id).hasClass('nvlnk-act')){
        $('#docCard'+lid).removeClass('show');
        $('#collapseAudio'+lid).removeClass('show');
        $('#buttonCollapseAudio'+lid).removeClass('nvlnk-act');
        $('#docTab'+lid).removeClass('nvlnk-act');
        $('#collapseVideo'+lid).removeClass('show');
        $('#buttonCollapseVideo'+lid).removeClass('nvlnk-act');
        $('#docClose'+lid).hide();
        $('.vidosik').addClass('show active');
        $('.vidosikTab').addClass('nvlnk-act');
        $("#doc"+lid).removeClass('show active');
        $('.vidClose').show();
    }
}

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
var zoomS = 0;
var pageWidth = document.body.offsetWidth;
function zoom() {
    $("#header").toggle();
    $("#wrapper").toggleClass('book-mode');
};





