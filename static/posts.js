function get_posts() {
    if($(window).scrollTop() + $(window).height() > $(document).height() - 1000) {
	$.get(window.location.href,
	      {'post_count' : document.getElementsByClassName("post").length,
	       "url": window.location.href },
	      function(data) {
		  $("#post_list").append(data);
	      });
    }
}

$(document).ready(function() {
    get_posts();
    $(window).scroll(get_posts);
});
