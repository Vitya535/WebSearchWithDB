function downloadDocs() {
    $.get('/?last_doc_number=' + last_doc_number, (loaded_docs) => {
        appendDocsInfoToWebPage(loaded_docs);
    });
}