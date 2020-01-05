$(document).ready(function () {
    $("#rb_watch_history").click(function () {
        $(location).attr('href', '/watch_history');
    });

    $("#rb_search_history").click(function () {
        $(location).attr('href', '/search_history');
    });

    $('#search-history-query-btn, #watch-history-query-btn').click(function () {
        $('#history_search_query').val('');
    });
});
