$(document).ready(function () {
    $(".delete-doc").click(function () {
        $(this).parent().parent().remove();

        let nav_link = $(this).siblings(':first');
        let search_query = $(':first-child', $(nav_link)).text();
        $.post('/search_history', {search_query: search_query}, onDeleteFromSearchHistory);
    });

    $("#clear_history").click(function () {
        if (confirm("Вы уверены что хотите очистить историю поиска?")) {
            $.post('/clear_search_history', onDeleteFromSearchHistory)
        }
    });

    $("#track_history").click(function () {
        if (confirm("Вы уверены что не хотите отслеживать историю поиска?")) {

        }
    });

    function onDeleteFromSearchHistory() {
        let docs_container = $("#docs-container");
        if ($(docs_container).children('.row.py-5, .row.pt-5').length === 0) {
            $(docs_container).empty();
            $(docs_container).append("<div class='row'><div class='col offset-1'><h2 class='pt-2'>История поиска</h2></div></div>" +
                "<div class='row align-items-center mt-5'>" +
                "<div class='col-12'><h4 class='text-center'>История поиска пуста!</h4>" +
                "</div></div>");
        }
    }
});