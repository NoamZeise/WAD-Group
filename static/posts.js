//flag if we are getting posts, so we do not get the same posts mutliple times
var getting_posts = false;
// so we can abort the current ajax request if needed
var current_post_request = null;
var to_clear = false;
function get_posts() {
    // if clear_posts was called, or
    //if posts aren't being retrieved, and the user has scrolled far enough to load more posts
    if(to_clear || (!getting_posts && $(window).scrollTop() + $(window).height() > $(document).height() - 1000)) {
	getting_posts = true;
	post_count = to_clear ? 0 : document.getElementsByClassName("post").length;
	current_post_request = $.get(window.location.href,
				     {"post_count" : post_count,
				      "url": window.location.href },
				     function(data) {
					 if(to_clear) {
					     document.getElementById("post_list").innerHTML = ""
					     to_clear = false;
					 }
					 $("#post_list").append(data);
					 getting_posts = false;
				     });
    }
}

function abort_post_request() {
    if(current_post_request != null) {
	current_post_request.abort();
	getting_posts = false;
    }
}

function clear_posts() {
    to_clear = true;
}

$(document).ready(function() {
    get_posts();
    $(window).scroll(get_posts);
});
