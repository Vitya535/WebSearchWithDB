"""Инициальзация частей приложения"""
from flask import Flask

# ToDo - 1. Сделать на стороне фронта правильное удаление в истории просмотра
#  (а не то, что сейчас) - также удалить на сервере.
# ToDo - 2. При очищении истории поиска очищать ее и на сервере тоже
# ToDo - 3. Окончательно разобраться с БД
# ToDo - 4. Заниматься бэком чтоли)
# ToDo - 5. Авторизация в пролете???

# ToDo - как инициализировать экзмепляр класса SQLAlchemy
#  без библиотеки Flask-SQLAlchemy? (если это вообще возможно)

APP = Flask(__name__)

if APP.config['ENV'] == 'production':
    APP.config.from_object('app.config.ProductionConfig')
elif APP.config['ENV'] == 'development':
    APP.config.from_object('app.config.DevelopmentConfig')
else:
    APP.config.from_object('app.config.TestingConfig')

from app import views
from app import errors
