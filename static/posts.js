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
    get_posts();
    $(window).scroll(get_posts);
});


$(document).ready(function() {
    $('#like_btn').click(function() {
        var postid;
        postid = $(this).attr('data-postid');
        $.get("/like-post/",
            {'post_id': postid},
            function(data) {
                $('#like_count').html(data);
                $('#like_btn').hide();
            })
    });
});

