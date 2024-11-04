from flask import Blueprint, render_template, request
from flask_paginate import Pagination, get_page_parameter
from app import db 

views_blueprint = Blueprint('views_front',__name__)


#Main Page
@views_blueprint.route('/', methods=['GET'])
def login():
    return render_template('auth/login.html')


#Docentes CRUD
@views_blueprint.route('/docentes', methods=['GET'])
def show_docentes():
    
    per_page = 4

    page = request.args.get(get_page_parameter(), type=int, default=1)
    offset = (page - 1) * per_page

    cursor = db.connection.cursor()
    query = "SELECT * FROM docente LIMIT %s OFFSET %s"
    cursor.execute(query, (per_page, offset))
    response = cursor.fetchall()


    teachers = [
        {
            'ID_docente': row[0],
            'Nombre': row[1],
            'Apellido': row[2],
            'Fecha_de_Nacimiento': row[3],
            'Correo': row[4],
            'Estado': row[5]
        }
        for row in response
    ]


    cursor.execute("SELECT COUNT(*) FROM docente")
    total_docentes = cursor.fetchone()[0]


    pagination = Pagination(page=page, total=total_docentes, per_page=per_page, css_framework='bootstrap4')

    return render_template('docentesCRUD/docentes.html', docentes=teachers, page=page, per_page=per_page, pagination=pagination)