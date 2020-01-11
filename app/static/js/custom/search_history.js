$(document).ready(function () {
    let csrftoken = $('meta[name=csrf-token]').attr('content');

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        }
    });

    $(".delete-doc").click(function () {
        $(this).parent().parent().remove();

        let nav_link = $(this).siblings(':first');
        let search_query = $(':first-child', $(nav_link)).text();
        $.post('/search_history', {search_query: search_query}, onDeleteFromSearchHistory);
    });

    $("#clear_history").click(function () {
        if (confirm("Вы уверены что хотите очистить историю поиска?")) {
            $.post('/clear_search_history', clearSearchHistory)
        }
    });

    $("#track_history").click(function () {
        if (confirm("Вы уверены что не хотите отслеживать историю поиска?")) {

        }
    });

    function onDeleteFromSearchHistory() {
        let docs_container = $("#docs-container");
        if ($(docs_container).children('.row.py-5, .row.pt-5').length === 0) {
            clearSearchHistory()
        }
    }

    function clearSearchHistory() {
        let docs_container = $("#docs-container");
        $(docs_container).children(':not(:first)').remove();
        $(docs_container).append(
            "<div class='row align-items-center mt-5'>\n" +
            "            <div class='col-12'>\n" +
            "                <h4 class='text-center'>История поиска пуста!</h4>\n" +
            "            </div>\n" +
            "        </div>");
    }
});