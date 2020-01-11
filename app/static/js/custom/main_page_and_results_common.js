let last_doc_number = 2;
const count_of_loaded_docs = 6;
let no_need_loading = false;

$(window).scroll(() => {
    let current_y = $(window).scrollTop();
    let window_height = $(window).height();
    let document_height = $(document).height();

    if (current_y + window_height === document_height) {
        if (no_need_loading) {
            $('.spinner-border').hide();
            $('#sentinel').hide();
            return;
        }
        downloadDocs();
        last_doc_number += count_of_loaded_docs;
    }
});

function appendDocsInfoToWebPage(loaded_docs) {
    if ($.isEmptyObject(loaded_docs)) {
        no_need_loading = true;
        $('.spinner-border').hide();
        $('#sentinel').hide();
        return;
    }
    let docs_container = $('#docs-container');
    $(docs_container).children('.row.py-5:first').removeClass('py-5').addClass('pt-5');
    $.each(loaded_docs, function () {
        let doc_row_for_append;
        $(docs_container).append('<div class="row pt-5">');
        doc_row_for_append = $(docs_container).children('.row.pt-5:last');
        $.each(this, function () {
            let document_for_append;
            $(doc_row_for_append).append('<div class="col">');
            document_for_append = $(doc_row_for_append).children('.col:last');
            $(document_for_append).append(
                '<a class="nav-link text-dark float-left pr-3 py-0 pl-0" href="/watch_file/' + this.path + '"' + '>' +
                '   <h6>' + this.doc_name + '</h6>' +
                '   <iframe width="600" height="450" src="/download_file/' + this.path + '#view=Fit"></iframe>\n' +
                '</a>\n' +
                '<a class="nav-link text-dark download_icon_style" href="/download_file/' + this.path + '"' + ' download>' +
                '   <i class="fas fa-download"></i>\n' +
                '</a>\n' +
                '</div>');
        });
        $(docs_container).append('</div>');
    });
    $(docs_container).children('.row.pt-5:last').removeClass('pt-5').addClass('py-5');
    $(docs_container).children('.row.py-5', '.row.pt-5').children('.col:first').addClass('offset-1');
}