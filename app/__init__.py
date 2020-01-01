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

# ToDo - не показывает Word и ODT-файлы в вебе, проверить другие форматы файлов (нашел какой-то ViewerJS, может поможет)
#  Может вообще не заморачиваться и пусть только 1 формат файлов будет???
# ToDo - Авторизация???
# ToDo - секьюрити???
# ToDo - сделать так чтобы при добавлении доков в папку они добавлялись в базу???
#  Ну и вообще чтобы доки, которые находятся в папке, при инициализации приложения всегда были в БД???
#  (думаю это не нужно, по крайней мере пока)
# ToDo - фильтрация по расширению файла при поиске???
# ToDo - странички ошибок по возможности покрасивее сделать и получше
# ToDo - может какие-нибудь сортировки этих файлов, различные вьюхи???
# ToDo - оптимизация, рефакторинг по возможности

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
debug_handler = RotatingFileHandler('app/logs/debug.log', maxBytes=10000, backupCount=1)
debug_handler.setLevel(DEBUG)
debug_handler.setFormatter(formatter)
LOG.addHandler(debug_handler)

error_handler = RotatingFileHandler('app/logs/error.log', maxBytes=10000, backupCount=1)
error_handler.setLevel(ERROR)
error_handler.setFormatter(formatter)
LOG.addHandler(error_handler)

from app import views
from app import errors
