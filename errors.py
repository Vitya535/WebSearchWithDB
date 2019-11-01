from app import app


@app.errorhandler(404)
def not_found_error(error):
    return 'Not Found!!!'


@app.errorhandler(500)
def internal_server_error(error):
    return 'Internal Server Error!!!'
