function downloadDocs() {
    let search_query = $('#search_query').val();
    $.get('/results?last_doc_number=' + last_doc_number + '&search_query=' + search_query, (loaded_docs) => {
        appendDocsInfoToWebPage(loaded_docs);
    });
}