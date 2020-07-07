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
		elem = 15;
	}
	if (elem == 3){
		elem = 20;
	}
	document.getElementById('val').innerHTML = elem;
}