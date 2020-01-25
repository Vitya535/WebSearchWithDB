"""Генерация и минификация CSS и JS файлов"""
from flask_assets import Bundle
from flask_assets import Environment

BUNDLES = {
    'cdn_common_css': Bundle(
        'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.4.1/css/bootstrap.min.css',
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.12.0-1/css/fontawesome.min.css',
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.12.0-1/css/solid.min.css',
        'https://cdnjs.cloudflare.com/ajax/libs/viewerjs/1.5.0/viewer.min.css',
        output='gen/css/common.css',
        filters='cssmin'
    ),
    'main_page_and_results_css': Bundle(
        'css/custom/main_page.css',
        'css/custom/common.css',
        output='gen/css/main_page_and_results.css',
        filters='cssmin'
    ),
    'history_common_css': Bundle(
        'css/custom/main_page.css',
        'css/custom/history.css',
        'css/custom/common.css',
        output='gen/css/history_common.css',
        filters='cssmin'
    ),
    'errors_css': Bundle(
        'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.4.1/css/bootstrap.min.css',
        'css/custom/errors.css',
        output='gen/css/errors.css',
        filters='cssmin'
    ),
    'cdn_common_js': Bundle(
        'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.4.1/js/bootstrap.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.12.0-1/js/fontawesome.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.12.0-1/js/solid.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/viewerjs/1.5.0/viewer.min.js',
        output='gen/js/common.js',
        filters='jsmin'
    ),
    'watch_history_js': Bundle(
        'js/custom/common.js',
        'js/custom/history.js',
        'js/custom/watch_history.js',
        output='gen/js/watch_history.js',
        filters='jsmin'
    ),
    'search_history_js': Bundle(
        'js/custom/common.js',
        'js/custom/history.js',
        'js/custom/search_history.js',
        output='gen/js/search_history.js',
        filters='jsmin'
    ),
    'main_page_js': Bundle(
        'js/custom/common.js',
        'js/custom/main_page_and_results_common.js',
        'js/custom/docs_lazy_load_main_page.js',
        output='gen/js/main_page.js',
        filters='jsmin'
    ),
    'results_js': Bundle(
        'js/custom/common.js',
        'js/custom/main_page_and_results_common.js',
        'js/custom/docs_lazy_load_results.js',
        output='gen/js/results.js',
        filters='jsmin'
    ),
    'errors_js': Bundle(
        'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.min.js',
        'js/custom/errors.js',
        output='gen/js/errors.js',
        filters='jsmin'
    ),
}
ASSETS = Environment()
ASSETS.register(BUNDLES)
