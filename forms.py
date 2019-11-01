from wtforms import Form
from wtforms.fields import StringField
from wtforms.fields.html5 import SearchField
from wtforms.widgets import html_params, HTMLString


class ButtonWidget(object):
    input_type = 'submit'
    html_params = staticmethod(html_params)

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('type', self.input_type)
        if 'value' not in kwargs:
            kwargs['value'] = field._value()

        return HTMLString('<button {params}>{label}</button>'.format(
            params=self.html_params(name=field.name, **kwargs),
            label=field.label.text)
        )


class ButtonField(StringField):
    widget = ButtonWidget()


class SearchForm(Form):
    search_query = SearchField(render_kw={'placeholder': 'Введите запрос', 'class': 'form-control'})
    search_button = ButtonField('<i class="fas fa-search"></i>', render_kw={'class': 'btn btn-light border'})


class HistorySearchForm(Form):
    history_search_query = SearchField(
        render_kw={'placeholder': 'Что найти в истории?', 'class': 'form-control mt-4 mx-auto',
                   'id': 'history_search_query'})
    history_search_button = ButtonField('<i class="fas fa-search"></i>', render_kw={'class': 'btn btn-light border'})
