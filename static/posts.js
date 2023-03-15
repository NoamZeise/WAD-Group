var getting_posts = false;
function get_posts() {
    if(!getting_posts && $(window).scrollTop() + $(window).height() > $(document).height() - 1000) {
	getting_posts = true;
	
	$.get(window.location.href,
	      {'post_count' : document.getElementsByClassName("post").length,
	       "url": window.location.href },
	      function(data) {
		  $("#post_list").append(data);
		  getting_posts = false;
	      });
    }
}

$(document).ready(function() {
    alert("hello"):
    get_posts();
    $(window).scroll(get_posts);
});


