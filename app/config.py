"""Различные конфигурации для проекта"""
from os import urandom


class Config:
    """Основной общий класс конфигурации"""
    SECRET_KEY = urandom(16)
    CLIENT_IMAGES = 'test_files/'
    CSRF_ENABLED = True


class ProductionConfig(Config):
    """Класс для работы приложения в Production"""
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """Класс для работы приложения в разработке"""
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Класс для тестирования приложения"""
    DEBUG = False
    TESTING = True
