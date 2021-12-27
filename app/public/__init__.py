# app/public/__init__.py

from flask import Blueprint

home = Blueprint('public', __name__)

from . import views
