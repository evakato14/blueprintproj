$(document).ready(function() {
    $('form').on('submit', function(event) {
    	$.ajax({
			data : {
                city : document.getElementById("city").value,
                county : document.getElementById("county").value,
			},
			type : 'POST',
			url : '/process'
		})
		.done(function(data) {
			//enter output here
		});
		event.preventDefault();
	})
});
