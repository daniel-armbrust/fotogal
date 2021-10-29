#
# fotogal/app/api/__init__.py
#

from flask import Blueprint
from flask import current_app as app

api = Blueprint('api', __name__)

from . import views, errors