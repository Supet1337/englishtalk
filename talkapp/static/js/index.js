$(document).ready(function(){
    $('a[href^="#s"]').click(function () {
	    elementClick = $(this).attr("href");
	    destination = $(elementClick).offset().top;
	    $('html').animate( { scrollTop: destination }, 1500 );
	    return false;
	});
});

var time = 0;
var pack = 3;
function calccost(){
    if(time == 0 && pack == 0){
	    document.getElementById('cost').innerHTML = "860 ₽";
    }
    else if(time == 0 && pack == 1){
	    document.getElementById('cost').innerHTML = "800 ₽";
    }
    else if(time == 0 && pack == 2){
        document.getElementById('cost').innerHTML = "740 ₽";
    }
    else if(time == 0 && pack == 3){
	    document.getElementById('cost').innerHTML = "660 ₽";
    }
    else if(time == 1 && pack == 0){
	    document.getElementById('cost').innerHTML = "920 ₽";
    }
    else if(time == 1 && pack == 1){
	    document.getElementById('cost').innerHTML = "880 ₽";
    }
    else if(time == 1 && pack == 2){
	    document.getElementById('cost').innerHTML = "820 ₽";
    }
    else if(time == 1 && pack == 3){
	    document.getElementById('cost').innerHTML = "740 ₽";
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

var slider = document.getElementById("customRange2");
slider.oninput = function() {
    changepack(slider.value)
}

function val(){
	elem = document.getElementById('customRange2').value;
	if (elem == 0){
		elem = 5;
	}
	if (elem == 1){
		elem = 10;
	}
	if (elem == 2){
		elem = 20;
	}
	if (elem == 3){
		elem = 30;
	}
	document.getElementById('val').innerHTML = elem;
}