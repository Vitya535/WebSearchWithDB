"""Инициализация частей приложения"""
from logging import DEBUG
from logging import ERROR
from logging import Formatter
from logging.handlers import RotatingFileHandler
from os.path import dirname

from flask import Flask
from flask.logging import create_logger
from flask_cdn import CDN
from flask_compress import Compress
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from app.assets import ASSETS

# ToDo - не показывает Word и ODT-файлы в вебе,
#  проверить другие форматы файлов (нашел какой-то ViewerJS, может поможет)
#  Может вообще не заморачиваться и пусть только 1 формат файлов будет???
# ToDo - Авторизация???
# ToDo - секьюрити???
# ToDo - фильтрация по расширению файла при поиске???
# ToDo - странички ошибок по возможности покрасивее сделать и получше
# ToDo - может какие-нибудь сортировки этих файлов, различные вьюхи???
# ToDo - оптимизация, рефакторинг по возможности

# ToDo:
#  Нашел я тут гугловские тулы - думаю надо поработать со страничками например, с помощью Lighthouse и др.
#  (С помощью Lighthouse и других тулов можно пооптимизировать в конце работу приложения,
#  особенно performance веб-страничек при различных скоростях интернета с помощью Lighthouse)

APP = Flask(__name__)

if APP.config['ENV'] == 'production':
    APP.config.from_object('app.config.ProductionConfig')
else:
    APP.config.from_object('app.config.DevelopmentConfig')

ASSETS.init_app(APP)

DB = SQLAlchemy(APP)
MA = Marshmallow(APP)
CDN = CDN(APP)
LOG = create_logger(APP)
CSRF = CSRFProtect(APP)
COMPRESS = Compress(APP)

FORMATTER = Formatter("%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s",
                      "%Y-%m-%d %H:%M:%S")
DEBUG_HANDLER = RotatingFileHandler(dirname(__file__) + '/logs/debug.log', maxBytes=100000, backupCount=5)
DEBUG_HANDLER.setLevel(DEBUG)
DEBUG_HANDLER.setFormatter(FORMATTER)
LOG.addHandler(DEBUG_HANDLER)

ERROR_HANDLER = RotatingFileHandler(dirname(__file__) + '/logs/error.log', maxBytes=100000, backupCount=5)
ERROR_HANDLER.setLevel(ERROR)
ERROR_HANDLER.setFormatter(FORMATTER)
LOG.addHandler(ERROR_HANDLER)

from app.views import *
from app.errors import *
