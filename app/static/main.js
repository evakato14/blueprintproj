function photo() {
    document.getElementById("typeIn").style.visibility = "hidden";
    document.getElementById("typeIn").style.display = "none";
    document.getElementById("toPhoto").style.visibility = "hidden";
    document.getElementById("toPhoto").style.display = "none";
    document.getElementById("toText").style.visibility = "visible";
    document.getElementById("toText").style.display = "block";
    document.getElementById("imageUpload").style.visibility = "visible";
    document.getElementById("imageUpload").style.display = "block";
}

function text() {
    document.getElementById("imageUpload").style.visibility = "hidden";
    document.getElementById("imageUpload").style.display = "none";
    document.getElementById("toText").style.visibility = "hidden";
    document.getElementById("toText").style.display = "none";
    document.getElementById("toPhoto").style.visibility = "visible";
    document.getElementById("toPhoto").style.display = "block";
    document.getElementById("typeIn").style.visibility = "visible";
    document.getElementById("typeIn").style.display = "block";
}

$(document).ready(function() {
    $('form').on('submit', function(event) {
    	$.ajax({
			data : {
                city : document.getElementById("city").value,
                county : document.getElementById("county").value,
                state : document.getElementById("state").value,
                material : document.getElementById("material").value
			},
			type : 'POST',
			url : '/retrieve'
		})
		.done(function(data) {
			$('#recyclingInfo').text(data.success).show();
		});
		event.preventDefault();
	})
});
