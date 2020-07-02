$(document).ready(function(){
    $('a[href^="#s"]').click(function () {
	    elementClick = $(this).attr("href");
	    destination = $(elementClick).offset().top;
	    $('html').animate( { scrollTop: destination }, 1500 );
	    return false;
	});
});

var time = 0;
var pack = 0;
function calccost(){
    if(time == 0 && pack == 0){
	    document.getElementById('cost').innerHTML = "770 ₽";
    }
    else if(time == 0 && pack == 1){
	    document.getElementById('cost').innerHTML = "680 ₽";
    }
    else if(time == 0 && pack == 2){
        document.getElementById('cost').innerHTML = "580 ₽";
    }
    else if(time == 0 && pack == 3){
	    document.getElementById('cost').innerHTML = "450 ₽";
    }
    else if(time == 1 && pack == 0){
	    document.getElementById('cost').innerHTML = "880 ₽";
    }
    else if(time == 1 && pack == 1){
	    document.getElementById('cost').innerHTML = "770 ₽";
    }
    else if(time == 1 && pack == 2){
	    document.getElementById('cost').innerHTML = "670 ₽";
    }
    else if(time == 1 && pack == 3){
	    document.getElementById('cost').innerHTML = "540 ₽";
    }
}

function changetime(nt){
    time = nt;
    calccost();
}
function changepack(np){
    pack = np;
    calccost();
}