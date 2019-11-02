"""Файл с веб-страничками для приложения"""
from flask import abort
from flask import render_template
from flask import send_from_directory

from app import APP
from app.forms import HistorySearchForm
from app.forms import SearchForm


@APP.route('/')
def main_page():
    """Главная веб-страничка"""
    search_form = SearchForm()
    return render_template('public/main_page.html', search_form=search_form)


# request.args.get('search_query', '')
@APP.route('/results')
def search_by_query():
    """Веб-страница с результатами поиска по названию файла"""
    search_form = SearchForm()
    return render_template('public/results.html', search_form=search_form)


@APP.route('/watch_history')
def show_watch_history():
    """Веб-страничка с историей просмотра документов"""
    search_form = SearchForm()
    search_in_history_form = HistorySearchForm()
    return render_template('public/watch_history.html',
                           search_form=search_form,
                           search_in_history_form=search_in_history_form)


@APP.route('/search_history')
def show_search_history():
    """Веб-страничка с историей поиска документов"""
    search_form = SearchForm()
    search_in_history_form = HistorySearchForm()
    return render_template('public/search_history.html',
                           search_form=search_form,
                           search_in_history_form=search_in_history_form)


@APP.route('/test_files/<filename>')
def watch_file(filename):
    """Веб-страничка для просмотра содержимого файла"""
    try:
        return send_from_directory(APP.config['CLIENT_IMAGES'], filename=filename)
    except FileNotFoundError:
        abort(404)
