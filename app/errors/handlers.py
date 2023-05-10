from flask import request, jsonify
from app.errors import bp
from app.constants.http_status_codes import *

# @bp.errorhandler(RootException)
# def handle_404(error):
#     return jsonify({'error': 'Not found.'}), HTTP_404_NOT_FOUND

@bp.app_errorhandler(500)
def handle_500(error):
    return jsonify({'error': 'Internal server error. Something went wrong.'}), HTTP_500_INTERNAL_SERVER_ERROR

@bp.app_errorhandler(404)
def handle_404(error):
    return {'error': 'Not found.'}, 404