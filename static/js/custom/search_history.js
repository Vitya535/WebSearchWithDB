$(document).ready(function () {
    $(".delete-doc").click(function () {
        $(this).parent().parent().remove();
    });

    $("#clear_history").click(function () {
        if (confirm("Вы уверены что хотите очистить историю поиска?")) {
            $("#docs-container").empty();
            $("#docs-container").append("<div class='row'><div class='col offset-1'><h2 class='pt-2'>История поиска</h2></div></div><div class='row align-items-center mt-5'><div class='col-12'><h4 class='text-center'>История пуста!</h4></div></div>");
        }
    });

    $("#track_history").click(function () {
        if (confirm("Вы уверены что не хотите отслеживать историю поиска?")) {

        }
    });

    $("#history_search_query").input(function () {
        alert('Ввод!');
    });
});