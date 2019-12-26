$(document).ready(function () {
    $("#rb_watch_history").click(function () {
        $(location).attr('href', '/watch_history');
    });

    $("#rb_search_history").click(function () {
        $(location).attr('href', '/search_history');
    });
});
