"""Различные конфигурации для проекта"""
from os import environ
from os import getcwd
from os import urandom
from os.path import dirname
from os.path import join

BASEDIR = dirname(__file__)
DOCUMENTS_DB = 'documents.db'
TEST_DB_DIR = 'test/test.db'
environ['LD_LIBRARY_PATH'] = getcwd()


class Config:
    """Основной общий класс конфигурации"""
    SECRET_KEY = urandom(16)
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(BASEDIR, DOCUMENTS_DB)
    CDN_HTTPS = True
    CDN_TIMESTAMP = False
    CDN_DOMAIN = 'cdnjs.cloudflare.com'
    CDN_ENDPOINTS = ['ajax/libs/jquery/3.4.1/jquery.min.js',
                     'ajax/libs/popper.js/1.14.7/umd/popper.min.js',
                     'ajax/libs/twitter-bootstrap/4.4.1/js/bootstrap.min.js',
                     'ajax/libs/font-awesome/5.11.2/js/all.min.js',
                     'ajax/libs/viewerjs/1.5.0/viewer.min.js',
                     'ajax/libs/twitter-bootstrap/4.4.1/css/bootstrap.min.css',
                     'ajax/libs/font-awesome/5.11.2/css/all.min.css',
                     'ajax/libs/viewerjs/1.5.0/viewer.min.css']


class ProductionConfig(Config):
    """Класс для работы приложения в Production"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ASSETS_DEBUG = False
    CDN_DEBUG = False
    MINIFY_HTML = True


class DevelopmentConfig(Config):
    """Класс для работы приложения в разработке"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    ASSETS_DEBUG = True
    CDN_DEBUG = True
    MINIFY_HTML = False


class TestingConfig(Config):
    """Класс для тестирования приложения"""
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ASSETS_DEBUG = False
    CDN_DEBUG = False
    MINIFY_HTML = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(BASEDIR, TEST_DB_DIR)
