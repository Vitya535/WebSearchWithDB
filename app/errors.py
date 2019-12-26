"""Класс для обработки ошибок в приложении"""
from flask import render_template
from flask import request

from app import APP
from app import LOG


@APP.errorhandler(404)
def not_found_error(error):
    """Класс для обработки ошибки 404 (Not Found)"""
    LOG.error(f"route: {request.url}, args: {request.args}, method: {request.method}, Not Found error: {error}")
    return render_template('errors/error_404.html'), 404


@APP.errorhandler(500)
def internal_server_error(error):
    """Класс для обработки ошибки 500 (Internal Server Error)"""
    LOG.error(f"route: {request.url}, args: {request.args}, method: {request.method}, Internal Server error: {error}")
    return render_template('errors/error_500.html'), 500
