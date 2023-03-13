function get_posts() {
    if($(window).scrollTop() + $(window).height() == $(document).height()) {
	$.get(window.location.href,
	      {'post_count' : document.getElementsByClassName("post").length,
	       "url": window.location.href },
	      function(data) {
		  $("#post_list").append(data);
	      });
    }
}

$(document).ready(get_posts);

$(document).ready(function() {
    $(window).scroll(get_posts);
});
