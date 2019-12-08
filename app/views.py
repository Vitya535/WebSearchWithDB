"""Файл с веб-страничками для приложения"""
from math import ceil

from flask import abort
from flask import jsonify
from flask import render_template
from flask import request
from flask import send_from_directory

from app import APP
from app.forms import HistorySearchForm
from app.forms import SearchForm
from app.orm_db_actions import delete_search_history_record_by_name
from app.orm_db_actions import delete_watch_history_record_by_name
from app.orm_db_actions import get_all_search_history_records
from app.orm_db_actions import get_all_watch_history_records
from app.orm_db_actions import get_search_history_records_by_name
from app.orm_db_actions import get_watch_history_records_by_name
from app.orm_db_actions import search_all_documents
from app.orm_db_actions import search_documents_by_name


@APP.route('/')
def main_page():
    """Главная веб-страничка"""
    search_form = SearchForm(request.args)
    all_documents = search_all_documents()
    count_of_rows = ceil(len(all_documents) / 4)
    return render_template('public/main_page.html',
                           search_form=search_form,
                           documents=all_documents,
                           count_of_rows=count_of_rows)


# request.args.get('search_query', '')
@APP.route('/results')
def search_by_query():
    """Веб-страница с результатами поиска по названию файла"""
    search_form = SearchForm(request.args)
    doc_name = request.args.get('search_query')
    documents = search_documents_by_name(doc_name)
    count_of_rows = ceil(len(documents) / 4)
    return render_template('public/results.html',
                           search_form=search_form,
                           documents=documents,
                           count_of_rows=count_of_rows)


# request.args.get('search_query', '')
@APP.route('/search_history_results')
def search_in_search_history_by_query():
    """Веб-страница с результатами поиска по названию файла"""
    search_form = SearchForm(request.args)
    search_in_history_form = HistorySearchForm(request.args)
    doc_name = request.args.get('search_query')
    search_history_records = get_search_history_records_by_name(doc_name)
    return render_template('public/search_history_results.html',
                           search_form=search_form,
                           search_in_history_form=search_in_history_form,
                           search_history_records=search_history_records)


# request.args.get('search_query', '')
@APP.route('/watch_history_results')
def search_in_watch_history_by_query():
    """Веб-страница с результатами поиска по названию файла"""
    search_form = SearchForm(request.args)
    search_in_history_form = HistorySearchForm(request.args)
    doc_name = request.args.get('search_query')
    watch_history_records = get_watch_history_records_by_name(doc_name)
    return render_template('public/watch_history_results.html',
                           search_form=search_form,
                           search_in_history_form=search_in_history_form,
                           watch_history_records=watch_history_records)


@APP.route('/watch_history', methods=['GET', 'POST'])
def show_watch_history():
    """Веб-страничка с историей просмотра документов"""
    if request.method == 'GET':
        search_form = SearchForm(request.args)
        search_in_history_form = HistorySearchForm(request.args)
        all_watch_history_records = get_all_watch_history_records()
        return render_template('public/watch_history.html',
                               search_form=search_form,
                               search_in_history_form=search_in_history_form,
                               watch_history_records=all_watch_history_records)
    print('POST')
    record_name = request.json
    print(record_name)
    delete_watch_history_record_by_name(record_name)
    # удалить запись о документе
    return jsonify({'data': 1})


@APP.route('/search_history', methods=['GET', 'POST'])
def show_search_history():
    """Веб-страничка с историей поиска документов"""
    if request.method == 'GET':
        search_form = SearchForm(request.args)
        search_in_history_form = HistorySearchForm(request.args)
        all_search_history_records = get_all_search_history_records()
        return render_template('public/search_history.html',
                               search_form=search_form,
                               search_in_history_form=search_in_history_form,
                               search_history_records=all_search_history_records)
    print('POST')
    record_name = request.json
    print(record_name)
    delete_search_history_record_by_name(record_name)
    # удалить запись о документе
    return jsonify()


@APP.route('/test_files/<filename>')
def watch_file(filename):
    """Веб-страничка для просмотра содержимого файла"""
    try:
        return send_from_directory(APP.config['CLIENT_IMAGES'], filename=filename)
    except FileNotFoundError:
        abort(404)
