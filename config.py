from os import urandom


class Config(object):
    SECRET_KEY = urandom(16)
    CLIENT_IMAGES = 'test_files/'
    CSRF_ENABLED = True


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    DEBUG = False
    TESTING = True
