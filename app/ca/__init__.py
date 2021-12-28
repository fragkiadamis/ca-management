# app/ca/__init__.py

from flask import Blueprint

admin = Blueprint('ca', __name__)

from . import views
