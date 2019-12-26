$(document).ready(function () {
    $(".delete-doc").click(function () {
        $(this).parent().parent().remove();

        let nav_link = $(this).siblings()[0];
        let search_query = $(nav_link).children('h6').text();
        $.post('/search_history', {search_query: search_query});
    });

    $("#clear_history").click(function () {
        if (confirm("Вы уверены что хотите очистить историю поиска?")) {
            $.post('/clear_search_history', onSuccessClearSearchHistory)
        }

        function onSuccessClearSearchHistory() {
            $("#docs-container").empty();
            $("#docs-container").append("<div class='row'><div class='col offset-1'><h2 class='pt-2'>История поиска</h2></div></div><div class='row align-items-center mt-5'><div class='col-12'><h4 class='text-center'>История пуста!</h4></div></div>");
        }
    });

    $("#track_history").click(function () {
        if (confirm("Вы уверены что не хотите отслеживать историю поиска?")) {

        }
    });
});