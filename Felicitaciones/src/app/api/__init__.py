from flask import Blueprint

docentes_api = Blueprint('docentes', __name__)

#Routes from docentes.py
from app.api import docentes

#Comprobar cumpleaños
from app.api import birthday_check 