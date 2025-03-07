"""Файл с различными формами, необходимыми для приложения"""
from wtforms import Form
from wtforms.fields import StringField
from wtforms.fields.html5 import SearchField
from wtforms.validators import InputRequired
from wtforms.widgets import HTMLString
from wtforms.widgets import html_params


class ButtonWidget:
    """Класс, реализующий кнопку типа <button {params}>{label}</button>"""
    html_params = staticmethod(html_params)

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        if 'value' not in kwargs:
            kwargs['value'] = field._value()

        return HTMLString('<button {params}>{label}</button>'.format(
            params=self.html_params(**kwargs),
            label=field.label.text))


class ButtonField(StringField):
    """Класс, создающий из кнопки поле"""
    widget = ButtonWidget()


class SearchForm(Form):
    """Класс, реализующий поисковую форму"""
    search_query = SearchField(render_kw={'placeholder': 'Введите запрос', 'class': 'form-control'},
                               validators=[InputRequired()])
    search_button = ButtonField('<i class="fas fa-search"></i>',
                                render_kw={'class': 'btn btn-light border', 'aria-label': 'Search for docs'})


class HistorySearchForm(Form):
    """Класс, реализующий форму поиска в истории поиска/просмотра"""
    history_search_query = SearchField(
        render_kw={'placeholder': 'Что найти в истории?', 'class': 'form-control mt-4 mx-auto',
                   'id': 'history_search_query'}, validators=[InputRequired()])
    history_search_button = ButtonField('<i class="fas fa-search"></i>',
                                        render_kw={'class': 'btn btn-light border', 'aria-label': 'Search in history'})
