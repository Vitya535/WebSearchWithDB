"""Генерация и минификация CSS и JS файлов"""
from flask_assets import Bundle
from flask_assets import Environment

BUNDLES = {
    'cdn_common_css': Bundle(
        'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.4.1/css/bootstrap.min.css',
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.11.2/css/all.min.css',
        output='gen/css/common.css',
        filters='cssmin'
    ),
    'cdn_common_js': Bundle(
        'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.4.1/js/bootstrap.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.11.2/js/all.min.js',
        output='gen/js/common.js',
        filters='jsmin'
    ),
    'main_page_and_results_css': Bundle(
        'css/libs/fontawesome/css/all.min.css',
        'css/custom/main_page.css',
        'css/custom/common.css',
        output='gen/css/main_page_and_results.css',
        filters='cssmin'
    ),
    'history_common_css': Bundle(
        'css/libs/fontawesome/css/all.min.css',
        'css/custom/main_page.css',
        'css/custom/history.css',
        'css/custom/common.css',
        output='gen/css/history_common.css',
        filters='cssmin'
    ),
    'watch_history_js': Bundle(
        'js/custom/common.js',
        'js/custom/history.js',
        'js/custom/watch_history.js',
        output='gen/css/watch_history.js',
        filters='jsmin'
    ),
    'search_history_js': Bundle(
        'js/custom/common.js',
        'js/custom/history.js',
        'js/custom/search_history.js',
        output='gen/css/search_history.js',
        filters='jsmin'
    )
}
ASSETS = Environment()
ASSETS.register(BUNDLES)

# viewer js
# https://cdnjs.cloudflare.com/ajax/libs/viewerjs/1.5.0/viewer.min.css
# https://cdnjs.cloudflare.com/ajax/libs/viewerjs/1.5.0/viewer.min.js
