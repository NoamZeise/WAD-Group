$(document).ready(function() {
	$(document).on("click", "button[use='follow']", function() {
		var username; 
		username = $(this).attr('user');
		var followButton = $(this);
		$.get('/follow/', 
			{'followname': username}, 
			function(data) {
				followButton.text(data);
			})
	});
});