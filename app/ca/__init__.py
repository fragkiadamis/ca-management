from flask import Blueprint

ca = Blueprint('ca', __name__)

from . import views
from . import members
from . import university_entities
from . import teams
from . import announcements
from . import activities
from . import files
