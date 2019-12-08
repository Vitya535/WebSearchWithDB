"""Различные конфигурации для проекта"""
from os import path
from os import urandom

BASEDIR = path.abspath(path.dirname(__file__))


class Config:
    """Основной общий класс конфигурации"""
    SECRET_KEY = urandom(16)
    CLIENT_IMAGES = 'test_files/'
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(BASEDIR, 'documents.db')


class ProductionConfig(Config):
    """Класс для работы приложения в Production"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Класс для работы приложения в разработке"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(Config):
    """Класс для тестирования приложения"""
    DEBUG = False
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
