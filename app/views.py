"""Файл с веб-страничками для приложения"""

from datetime import datetime

from flask import abort
from flask import jsonify
from flask import render_template
from flask import request
from flask import send_file
from htmlmin import minify

from app import APP
from app import LOG
from app.forms import HistorySearchForm
from app.forms import SearchForm
from app.orm_db_actions import add_search_history_record
from app.orm_db_actions import add_watch_history_record
from app.orm_db_actions import clear_all_in_search_history
from app.orm_db_actions import clear_all_in_watch_history
from app.orm_db_actions import delete_search_history_record_by_search_query
from app.orm_db_actions import delete_watch_history_record_by_doc_name
from app.orm_db_actions import get_all_search_history_records
from app.orm_db_actions import get_all_watch_history_records
from app.orm_db_actions import get_search_history_records_by_name
from app.orm_db_actions import get_watch_history_records_by_name
from app.orm_db_actions import search_document_by_path
from app.orm_db_actions import search_first_four_documents
from app.orm_db_actions import search_first_four_documents_by_partial_name
from app.orm_db_actions import search_six_documents_by_partial_name_from_number
from app.orm_db_actions import search_six_documents_from_number
from app.utils import convert_document_list_to_map
from app.utils import convert_document_map_to_json
from app.utils import divide_watch_history_records_by_datetime
from app.utils import update_datetime_in_search_history_records


@APP.after_request
def add_header(response):
    response.cache_control.max_age = 86400
    return response


@APP.route('/')
def main_page():
    """Главная веб-страничка"""
    LOG.debug(f"Enter into main_page "
              f"with url={request.url}, args={request.args}, method={request.method}")
    search_form = SearchForm(request.args)
    if not request.args:
        first_four_documents = search_first_four_documents()
        documents_map = convert_document_list_to_map(first_four_documents)
        LOG.debug(f"First_four_documents is {first_four_documents}")
        return minify(render_template('public/main_page.html',
                                      search_form=search_form,
                                      documents=documents_map))
    last_doc_number = int(request.args.get('last_doc_number'))
    LOG.debug(f"last_doc_number={last_doc_number}")
    six_documents = search_six_documents_from_number(last_doc_number + 1)
    LOG.debug(f"Found 6 docs - {six_documents}")
    six_documents_map = convert_document_list_to_map(six_documents)
    jsonified_six_documents_map = convert_document_map_to_json(six_documents_map)
    LOG.debug(f"Jsonified map - {jsonified_six_documents_map}")
    return jsonified_six_documents_map


@APP.route('/results')
def search_by_query():
    """Веб-страница с результатами поиска по названию файла"""
    LOG.debug(f"Enter into search_by_query "
              f"with url={request.url}, args={request.args}, method={request.method}")
    search_form = SearchForm(request.args)
    search_query = request.args.get('search_query')
    if not request.args.get('last_doc_number'):
        # checked_extensions = request.args.get('checked_extensions')
        first_four_documents = search_first_four_documents_by_partial_name(search_query)
        documents_map = convert_document_list_to_map(first_four_documents)
        # f"checked_extensions={checked_extensions}, "
        LOG.debug(f"First_four_docs founded by search_query={search_query}, "
                  f"first_four_documents={first_four_documents}")
        add_search_history_record(search_query, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return minify(render_template('public/results.html',
                                      search_form=search_form,
                                      documents=documents_map))
    last_doc_number = int(request.args.get('last_doc_number'))
    LOG.debug(f"last_doc_number={last_doc_number}")
    six_documents = search_six_documents_by_partial_name_from_number(search_query, last_doc_number + 1)
    LOG.debug(f"Found 6 docs - {six_documents}")
    six_documents_map = convert_document_list_to_map(six_documents)
    jsonified_six_documents_map = convert_document_map_to_json(six_documents_map)
    LOG.debug(f"Jsonified map - {jsonified_six_documents_map}")
    return jsonified_six_documents_map


@APP.route('/search_history_results')
def search_in_search_history_by_query():
    """Веб-страница с результатами поиска по названию файла"""
    LOG.debug(f"Enter into search_in_search_history_query "
              f"with url={request.url}, args={request.args},"
              f" method={request.method}")
    search_form = SearchForm(request.args)
    search_in_history_form = HistorySearchForm(request.args)
    doc_name = request.args.get('history_search_query')
    search_history_records = get_search_history_records_by_name(doc_name)
    updated_search_history_records = \
        update_datetime_in_search_history_records(search_history_records)
    LOG.debug(f"All search history records founded by name={doc_name}: {search_history_records}")
    return minify(render_template('public/search_history_results.html',
                                  search_form=search_form,
                                  search_in_history_form=search_in_history_form,
                                  search_history_records=updated_search_history_records))


@APP.route('/watch_history_results')
def search_in_watch_history_by_query():
    """Веб-страница с результатами поиска по названию файла"""
    LOG.debug(f"Enter into search_in_watch_history_by_query "
              f"with url={request.url}, args={request.args},"
              f" method={request.method}")
    search_form = SearchForm(request.args)
    search_in_history_form = HistorySearchForm(request.args)
    doc_name = request.args.get('history_search_query')
    watch_history_records = get_watch_history_records_by_name(doc_name)
    watch_history_records_dict = divide_watch_history_records_by_datetime(watch_history_records)
    return minify(render_template('public/watch_history_results.html',
                                  search_form=search_form,
                                  search_in_history_form=search_in_history_form,
                                  watch_history_records_dict=watch_history_records_dict))


@APP.route('/watch_history', methods=['GET', 'POST'])
def show_watch_history():
    """Веб-страничка с историей просмотра документов"""
    LOG.debug(f"Enter into show_watch_history "
              f"with url={request.url}, args={request.args}, method={request.method}")
    if request.method == 'GET':
        search_form = SearchForm(request.args)
        search_in_history_form = HistorySearchForm(request.args)
        all_watch_history_records = get_all_watch_history_records()
        watch_history_records_dict = divide_watch_history_records_by_datetime(all_watch_history_records)
        return minify(render_template('public/watch_history.html',
                                      search_form=search_form,
                                      search_in_history_form=search_in_history_form,
                                      watch_history_records_dict=watch_history_records_dict))
    doc_name = request.values.get('doc_name')
    delete_watch_history_record_by_doc_name(doc_name)
    return jsonify()


@APP.route('/search_history', methods=['GET', 'POST'])
def show_search_history():
    """Веб-страничка с историей поиска документов"""
    LOG.debug(f"Enter into show_search_history "
              f"with url={request.url}, args={request.args}, method={request.method}")
    if request.method == 'GET':
        search_form = SearchForm(request.args)
        search_in_history_form = HistorySearchForm(request.args)
        all_search_history_records = get_all_search_history_records()
        updated_search_history_records = \
            update_datetime_in_search_history_records(all_search_history_records)
        LOG.debug(f"Updated search history records: {updated_search_history_records}")
        return minify(render_template('public/search_history.html',
                                      search_form=search_form,
                                      search_in_history_form=search_in_history_form,
                                      search_history_records=updated_search_history_records))
    search_query = request.values.get('search_query')
    delete_search_history_record_by_search_query(search_query)
    return jsonify()


@APP.route('/clear_search_history', methods=['POST'])
def clear_search_history():
    """Метод для очищения истории поиска"""
    LOG.debug(f"Enter into clear_search_history "
              f"with url={request.url}, args={request.args}, method={request.method}")
    clear_all_in_search_history()
    return jsonify()


@APP.route('/clear_watch_history', methods=['POST'])
def clear_watch_history():
    """Метод для очищения истории поиска"""
    LOG.debug(f"Enter into clear_watch_history "
              f"with url={request.url}, args={request.args}, method={request.method}")
    clear_all_in_watch_history()
    return jsonify()


@APP.route('/download_file/<path:path_to_file>')
def download_file(path_to_file):
    """Урл для первоначальной загрузки документов в iframe на страницах"""
    LOG.debug(f"Enter into download_file "
              f"with url={request.url}, args={request.args}, method={request.method},"
              f" path_to_file={path_to_file}")
    try:
        return send_file(path_to_file)
    except FileNotFoundError:
        LOG.error(f"File with path_to_file={path_to_file} not founded (404 Not Found)")
        abort(404)


@APP.route('/watch_file/<path:path_to_file>')
def watch_file(path_to_file):
    """Веб-страничка для просмотра содержимого файла"""
    LOG.debug(f"Enter into watch_file "
              f"with url={request.url}, args={request.args}, method={request.method},"
              f" path_to_file={path_to_file}")
    try:
        file = send_file(path_to_file)
        document_id = search_document_by_path(path_to_file).id
        LOG.debug(f"The path to file is {path_to_file} and it's id is {document_id}")
        add_watch_history_record(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), document_id)
        return file
    except FileNotFoundError:
        LOG.error(f"File with path_to_file={path_to_file} not founded (404 Not Found)")
        abort(404)
