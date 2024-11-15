from flask import Blueprint, render_template, request
from flask_paginate import Pagination, get_page_parameter
from app import db 
from flask_login import login_required

views_blueprint = Blueprint('views_front',__name__)


#Main Page
@views_blueprint.route('/', methods=['GET'])
def home():
    return render_template('auth/login.html')


#Tools
@views_blueprint.route('/tools', methods=['GET'])
@login_required
def register_admin():
    return render_template('main/tools.html')


#Docentes CRUD
@views_blueprint.route('/docentes', methods=['GET'])
@login_required
def show_docentes():
    return render_template('main/docentes.html')

#Felicitaciones Read
@views_blueprint.route('/felicitaciones', methods=['GET'])
@login_required
def show_felicitaciones():
    return render_template('main/felicitaciones.html')