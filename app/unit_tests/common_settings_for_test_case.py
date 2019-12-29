"""Общие начальные настройки для модульных тестов"""
from unittest import TestCase

from app import APP
from app import DB


class CommonSettingsForTestCase(TestCase):
    """Общие начальные настройки для модульных тестов"""

    def setUp(self):
        """Установка начальных настроек для тестов"""
        APP.config.from_object('app.config.TestingConfig')
        self.app = APP.test_client()
        DB.create_all()

    def tearDown(self):
        """Очистка начальных настроек и параметров"""
        DB.drop_all()
