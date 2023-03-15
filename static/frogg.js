$(document).ready(function() {
    alert('hello'):
    $('#like_btn').click(function() {
        var postid;
        postid = $(this).attr('data-postid');
        $.get(window.location.href,
            {'post_id': postid},
            function(data) {
                $('#like_count').html(data);
                $('#like_btn').hide();
            })
    });
});