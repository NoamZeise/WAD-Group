var search_page = "/search-results/";
var blanked = false;
const slugify = str =>
  str
    .toLowerCase()
    .trim()
    .replace(/[^\w\s-]/g, '')
    .replace(/[\s_-]+/g, '-')
      .replace(/^-+|-+$/g, '');
$(document).ready(function() {
    //    $("#searchbtn").css("visibility", "hidden")
    if(window.location.href.includes(search_page)) {
	var query = window.location.href;
	var end = query.indexOf('?');
	end = end == -1 ? query.length : end;
	query = query.slice(query.indexOf(search_page) + search_page.length, end);
	$('#searchbar').val(query);
	$('#searchbar').focus()
    }
    $('#searchbar').focus(function() {
	if(!window.location.href.includes(search_page)) {
	    $("#searchbtn").click()
	}});
    $('#searchbar').on('input', function() {
	// requires posts.js to be in scope
	// which happends when we redirect to search-results on input focus
	abort_post_request();
	clear_posts();
	// change url to current search term os posts ajax requests will use updated search query
	// also maintain any sorting functions added to the results
	var query = window.location.href;
	var end = query.indexOf('?');
	window.history.replaceState(null, null, search_page + slugify($("#searchbar").val())
				    + (end != -1 ? query.slice(end) : ""));
	$(window).scroll();
    });
});
