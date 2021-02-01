#
# fotogal/app/main/__init__.py
#

from flask import Blueprint
from flask import current_app as app

main = Blueprint('main', __name__)

from . import views, errors
