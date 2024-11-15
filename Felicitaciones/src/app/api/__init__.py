from flask import Blueprint

docentes_api = Blueprint('docentes', __name__)

#Routes from docentes.py
from . import docentes
from . import login
from . import felicitaciones




