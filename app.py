from flask import Flask

# ToDo - 1. Сделать на стороне фронта правильное удаление в истории просмотра (а не то, что сейчас) -
#  также удалить на сервере.
# ToDo - 2. При очищении истории поиска очищать ее и на сервере тоже
# ToDo - 3. Окончательно разобраться с БД
# ToDo - 4. Заниматься бэком чтоли)
# ToDo - 5. Авторизация в пролете???

# ToDo - как инициализировать экзмепляр класса SQLAlchemy без библиотеки Flask-SQLAlchemy? (если это вообще возможно)

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

from views import *
from errors import *

if __name__ == '__main__':
    app.run()
