from flask import Blueprint

docentes_api = Blueprint('docentes', __name__)

#Routes from docentes.py
from app.api import docentes


#Ruta para Login
from .login.login import login_blueprint


