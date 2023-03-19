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