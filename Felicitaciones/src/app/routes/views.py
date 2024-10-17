from flask import Blueprint,render_template

views_blueprint = Blueprint('views_front',__name__)


#Main Page
@views_blueprint.route('/', methods=['GET'])
def login():
    return render_template('auth/login.html')


#Docentes CRUD
@views_blueprint.route('/docentes', methods=['GET'])
def show_docentes():
    return render_template('docentesCRUD/docentes.html')