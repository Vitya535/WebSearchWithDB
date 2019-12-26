$(document).ready(function () {
    $('#search-query-btn').click(function () {
        $('#search_query').val('');
    });

    $('#search-history-query-btn').click(function () {
        $('#history_search_query').val('');
    });

    $('#watch-history-query-btn').click(function () {
        $('#history_search_query').val('');
    });

    $('#search_button').click(function () {
        let search_query = $('#search_query').val();
        alert('search_query is: ' + search_query);
        let checked_extensions = $('#modal_window_search_filter')
            .find('.form-check-input:checked')
            .siblings('span');
        alert('checked_extensions is: ' + checked_extensions);
        $.map(checked_extensions, function (value, index) {
            alert(value);
            alert(index);
            alert(value.val().toLowerCase());
            return value.val().toLowerCase();
        });
        alert('mapped checked_extensions is: ' + checked_extensions);
        $.get('/results', {search_query: search_query, checked_extensions: checked_extensions});
    })
});