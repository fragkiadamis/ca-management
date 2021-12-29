# app/ca/__init__.py

from flask import Blueprint

ca = Blueprint('ca', __name__)

from . import views
