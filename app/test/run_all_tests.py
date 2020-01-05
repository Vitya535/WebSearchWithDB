"""Файл для прогона всех тестов"""
from os.path import dirname
from unittest import TestLoader
from unittest import TestSuite
from unittest import TextTestRunner


def init_test_suite() -> TestSuite:
    """Функция для инициализации TestSuite, нужного для прогона всех тестов в директории test"""
    test_suite = TestLoader().discover(dirname(__file__))
    return test_suite


if __name__ == '__main__':
    suite = init_test_suite()
    runner = TextTestRunner()
    runner.run(suite)
