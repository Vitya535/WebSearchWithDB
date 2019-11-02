"""Класс для обработки ошибок в приложении"""
from flask import request

from app import APP


@APP.errorhandler(404)
def not_found_error(error):
    """Класс для обработки ошибки 404 (Not Found)"""
    APP.logger.error(f"route: {request.url}, Not Found error: {error}")
    return 'Not Found!!!', 404


@APP.errorhandler(500)
def internal_server_error(error):
    """Класс для обработки ошибки 500 (Internal Server Error)"""
    APP.logger.error(f"route: {request.url}, Not Found error: {error}")
    return 'Internal Server Error!!!', 500
