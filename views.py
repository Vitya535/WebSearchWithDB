from flask import render_template, send_from_directory, abort

from app import app
from forms import SearchForm, HistorySearchForm


@app.route('/')  # главная страница приложения
def main_page():
    search_form = SearchForm()
    return render_template('main_page.html', search_form=search_form)


# request.args.get('search_query', '')
@app.route('/results')
def search_by_query():
    search_form = SearchForm()
    return render_template('results.html', search_form=search_form)


@app.route('/watch_history')
def show_watch_history():
    search_form = SearchForm()
    search_in_history_form = HistorySearchForm()
    return render_template('watch_history.html', search_form=search_form, search_in_history_form=search_in_history_form)


@app.route('/search_history')
def show_search_history():
    search_form = SearchForm()
    search_in_history_form = HistorySearchForm()
    return render_template('search_history.html', search_form=search_form, search_in_history_form=search_in_history_form)


@app.route('/test_files/<filename>')
def watch_file(filename):
    try:
        return send_from_directory(app.config['CLIENT_IMAGES'], filename=filename)
    except FileNotFoundError:
        abort(404)
