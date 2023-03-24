$(document).ready(function() {
	$(document).on("click", "button[use='follow']", function() {
		var username; 
		username = $(this).attr('user');
		var followButton = $(this);
		$.get('/follow/', 
			{'followname': username}, 
		      function(data) {
			  var return_data = data.split(" ", 1);
			  var follow = return_data[0];
			  var rest = data.substring(data.indexOf(" "), data.length);
			  $("#follower_list").html(rest);
			  followButton.text(follow);
		      })
	});
});
