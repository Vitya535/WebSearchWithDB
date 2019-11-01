$(document).ready(function () {
    $("#rb_watch_history").click(function () {
        $(location).attr('pathname', '/watch_history');
    });

    $("#rb_search_history").click(function () {
        $(location).attr('pathname', '/search_history');
    });
});
