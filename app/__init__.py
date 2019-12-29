"""Инициальзация частей приложения"""
from logging import DEBUG
from logging import ERROR
from logging import Formatter
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask.logging import create_logger
from flask_cdn import CDN
from flask_htmlmin import HTMLMIN
from flask_sqlalchemy import SQLAlchemy

from app.assets import ASSETS

# ToDo - вставить как-то скрин 1-ой страницы или что-то в этом духе на месте img-шек доков
#  (нашел какой-то ViewerJS, может поможет)
# ToDo - не показывает Word-файл в вебе, проверить другие форматы файлов (нашел какой-то ViewerJS, может поможет)
# ToDo - Авторизация???
# ToDo - секьюрити???
# ToDo - странички ошибок по возможности покрасивее сделать и получше
# ToDo - тесты???
# ToDo - сделать так чтобы при добавлении доков в папку они добавлялись в базу???
#  Ну и вообще чтобы доки, которые находятся в папке, при инициализации приложения всегда были в БД???
# ToDo - фильтрация по расширению файла при поиске???
# ToDo - убрать кастомное поведение валидации у поискового поля или не убирать???
# ToDo - поправить доступ к переменным, методам если это возможно

APP = Flask(__name__)

if APP.config['ENV'] == 'production':
    APP.config.from_object('app.config.ProductionConfig')
else:
    APP.config.from_object('app.config.DevelopmentConfig')

ASSETS.init_app(APP)

DB = SQLAlchemy(APP)
CDN = CDN(APP)
LOG = create_logger(APP)
HTMLMIN = HTMLMIN(APP)

formatter = Formatter("%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")
debug_handler = RotatingFileHandler('logs/debug.log', maxBytes=10000, backupCount=1)
debug_handler.setLevel(DEBUG)
debug_handler.setFormatter(formatter)
LOG.addHandler(debug_handler)

error_handler = RotatingFileHandler('logs/error.log', maxBytes=10000, backupCount=1)
error_handler.setLevel(ERROR)
error_handler.setFormatter(formatter)
LOG.addHandler(error_handler)

from app import views
from app import errors
