from flask import Blueprint

ca = Blueprint('ca', __name__)

from . import views
from . import members
from . import university_entities
