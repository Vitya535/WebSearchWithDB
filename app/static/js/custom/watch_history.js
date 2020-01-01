$(document).ready(function () {
    $(".delete-doc").click(function () {
        $(this).parent().parent().remove();

        let nav_link = $(this).siblings(':first');
        let doc_name = $(nav_link).children(':first').text();
        $.post('/watch_history', {doc_name: doc_name}, onDeleteWatchHistory);

        function onDeleteWatchHistory() {
            let docs_container = $('#docs-container');
            if ($(docs_container).children('.row.py-5, .row.pt-5').length === 0) {
                $(docs_container).empty();
                $(docs_container).append("<div class='row'><div class='col offset-1'><h2 class='pt-2'>История просмотра</h2></div></div>" +
                    "<div class='row align-items-center mt-5'>\n" +
                    "            <div class='col-12'>\n" +
                    "                <h4 class='text-center'>История просмотров пуста!</h4>\n" +
                    "            </div>\n" +
                    "        </div>");
            }
        }
    });

    $("#clear_history").click(function () {
        if (confirm("Вы уверены что хотите очистить историю просмотров?")) {
            $.post('/clear_watch_history', onSuccessClearWatchHistory);
        }

        function onSuccessClearWatchHistory() {
            let docs_container = $("#docs-container");
            $(docs_container).empty();
            $(docs_container).append("<div class='row'><div class='col offset-1'><h2 class='pt-2'>История просмотра</h2></div></div><div class='row align-items-center mt-5'><div class='col-12'><h4 class='text-center'>История просмотров пуста!</h4></div></div>");
        }
    });

    $("#track_history").click(function () {
        if (confirm("Вы уверены что не хотите отслеживать историю просмотров?")) {

        }
    });
});