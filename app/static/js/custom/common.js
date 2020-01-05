$(document).ready(function () {
    $('#search-query-btn').click(function () {
        $('#search_query').val('');
    });

    $('#search_button').click(function () {
        let search_query = $('#search_query').val();
        $.get('/results', {search_query: search_query});
    })
});