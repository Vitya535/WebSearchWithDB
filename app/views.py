"""Файл с веб-страничками для приложения"""

from datetime import datetime
from os.path import splitext

from flask import abort
from flask import jsonify
from flask import render_template
from flask import request
from flask import send_from_directory

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
from app.orm_db_actions import search_all_documents
from app.orm_db_actions import search_document_by_full_name
from app.orm_db_actions import search_documents_by_partial_name
from app.utils import convert_document_list_to_map
from app.utils import divide_watch_history_records_by_datetime
from app.utils import update_datetime_in_search_history_records


@APP.route('/')
def main_page():
    """Главная веб-страничка"""
    LOG.debug(f"Enter into main_page with url={request.url}, args={request.args}, method={request.method}")
    search_form = SearchForm(request.args)
    all_documents = search_all_documents()
    all_documents_map = convert_document_list_to_map(all_documents)
    LOG.debug(f"All documents is {all_documents}")
    return render_template('public/main_page.html',
                           search_form=search_form,
                           documents=all_documents_map)


@APP.route('/results')
def search_by_query():
    """Веб-страница с результатами поиска по названию файла"""
    LOG.debug(f"Enter into search_by_query with url={request.url}, args={request.args}, method={request.method}")
    search_form = SearchForm(request.args)
    search_query = request.args.get('search_query')
    checked_extensions = request.args.get('checked_extensions')
    documents = search_documents_by_partial_name(search_query)
    documents_map = convert_document_list_to_map(documents)
    LOG.debug(f"All docs founded by search_query={search_query} and checked_extensions={checked_extensions}: "
              f"{documents}")
    add_search_history_record(search_query, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return render_template('public/results.html',
                           search_form=search_form,
                           documents=documents_map)


@APP.route('/search_history_results')
def search_in_search_history_by_query():
    """Веб-страница с результатами поиска по названию файла"""
    LOG.debug(f"Enter into search_in_search_history_query with url={request.url}, args={request.args},"
              f" method={request.method}")
    search_form = SearchForm(request.args)
    search_in_history_form = HistorySearchForm(request.args)
    doc_name = request.args.get('history_search_query')
    search_history_records = get_search_history_records_by_name(doc_name)
    updated_search_history_records = \
        update_datetime_in_search_history_records(search_history_records)
    LOG.debug(f"All search history records founded by name={doc_name}: {search_history_records}")
    return render_template('public/search_history_results.html',
                           search_form=search_form,
                           search_in_history_form=search_in_history_form,
                           search_history_records=updated_search_history_records)


@APP.route('/watch_history_results')
def search_in_watch_history_by_query():
    """Веб-страница с результатами поиска по названию файла"""
    LOG.debug(f"Enter into search_in_watch_history_by_query with url={request.url}, args={request.args},"
              f" method={request.method}")
    search_form = SearchForm(request.args)
    search_in_history_form = HistorySearchForm(request.args)
    doc_name = request.args.get('history_search_query')
    watch_history_records = get_watch_history_records_by_name(doc_name)
    watch_history_records_today, watch_history_records_yesterday, watch_history_records_days_ago = \
        divide_watch_history_records_by_datetime(watch_history_records)
    LOG.debug(f"Records for today is {watch_history_records_today},"
              f" for yesterday is {watch_history_records_yesterday},"
              f" days ago is {watch_history_records_days_ago}")
    return render_template('public/watch_history_results.html',
                           search_form=search_form,
                           search_in_history_form=search_in_history_form,
                           watch_history_records_today=watch_history_records_today,
                           watch_history_records_yesterday=watch_history_records_yesterday,
                           watch_history_records_days_ago=watch_history_records_days_ago)


@APP.route('/watch_history', methods=['GET', 'POST'])
def show_watch_history():
    """Веб-страничка с историей просмотра документов"""
    LOG.debug(f"Enter into show_watch_history with url={request.url}, args={request.args}, method={request.method}")
    if request.method == 'GET':
        search_form = SearchForm(request.args)
        search_in_history_form = HistorySearchForm(request.args)
        all_watch_history_records = get_all_watch_history_records()
        watch_history_records_today, watch_history_records_yesterday, watch_history_records_days_ago = \
            divide_watch_history_records_by_datetime(all_watch_history_records)
        LOG.debug(f"Records for today is {watch_history_records_today},"
                  f" for yesterday is {watch_history_records_yesterday},"
                  f" days ago is {watch_history_records_days_ago}")
        return render_template('public/watch_history.html',
                               search_form=search_form,
                               search_in_history_form=search_in_history_form,
                               watch_history_records_today=watch_history_records_today,
                               watch_history_records_yesterday=watch_history_records_yesterday,
                               watch_history_records_days_ago=watch_history_records_days_ago)
    doc_name = request.values.get('doc_name')
    delete_watch_history_record_by_doc_name(doc_name)
    return jsonify()


@APP.route('/search_history', methods=['GET', 'POST'])
def show_search_history():
    """Веб-страничка с историей поиска документов"""
    LOG.debug(f"Enter into show_search_history with url={request.url}, args={request.args}, method={request.method}")
    if request.method == 'GET':
        search_form = SearchForm(request.args)
        search_in_history_form = HistorySearchForm(request.args)
        all_search_history_records = get_all_search_history_records()
        updated_search_history_records = update_datetime_in_search_history_records(all_search_history_records)
        LOG.debug(f"Updated search history records: {updated_search_history_records}")
        return render_template('public/search_history.html',
                               search_form=search_form,
                               search_in_history_form=search_in_history_form,
                               search_history_records=updated_search_history_records)
    search_query = request.values.get('search_query')
    delete_search_history_record_by_search_query(search_query)
    return jsonify()


@APP.route('/clear_search_history', methods=['POST'])
def clear_search_history():
    """Метод для очищения истории поиска"""
    LOG.debug(f"Enter into clear_search_history with url={request.url}, args={request.args}, method={request.method}")
    clear_all_in_search_history()
    return jsonify()


@APP.route('/clear_watch_history', methods=['POST'])
def clear_watch_history():
    """Метод для очищения истории поиска"""
    LOG.debug(f"Enter into clear_watch_history with url={request.url}, args={request.args}, method={request.method}")
    clear_all_in_watch_history()
    return jsonify()


@APP.route('/download_file/<filename>')
def download_file(filename):
    """Урл для первоначальной загрузки документов в iframe на страницах"""
    LOG.debug(f"Enter into load_file_into_iframe with url={request.url}, args={request.args}, method={request.method},"
              f" filename={filename}")
    try:
        return send_from_directory(APP.config['CLIENT_IMAGES'], filename=filename)
    except FileNotFoundError:
        LOG.error(f"File with filename={filename} not founded (404 Not Found)")
        abort(404)


@APP.route('/watch_file/<filename>')
def watch_file(filename):
    """Веб-страничка для просмотра содержимого файла"""
    LOG.debug(f"Enter into watch_file with url={request.url}, args={request.args}, method={request.method},"
              f" filename={filename}")
    try:
        file = send_from_directory(APP.config['CLIENT_IMAGES'], filename=filename)
        doc_name = splitext(filename)[0]
        document_id = search_document_by_full_name(doc_name).id
        LOG.debug(f"The document name is {doc_name} and it's id is {document_id}")
        add_watch_history_record(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), document_id)
        return file
    except FileNotFoundError:
        LOG.error(f"File with filename={filename} not founded (404 Not Found)")
        abort(404)
