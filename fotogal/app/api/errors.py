#
# fotogal/app/api/errors.py
#

from flask import request, render_template, jsonify
from . import api

@api.app_errorhandler(404)
def not_found(e):
    if request.accept_mimetypes.accept_json and (not request.accept_mimetypes.accept_html):
        return jsonify({'status': '404', 'message': 'Not Found'}), 404   
    else:
        return render_template('404.html'), 404


@api.app_errorhandler(500)
def internal_server_error(e):
    if request.accept_mimetypes.accept_json and (not request.accept_mimetypes.accept_html):
        return jsonify({'status': '500', 'message': 'Internal Server Error'}), 500
    else:
        return render_template('404.html'), 404