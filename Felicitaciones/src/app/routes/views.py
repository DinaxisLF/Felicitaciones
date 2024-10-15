from flask import Blueprint,render_template

views_blueprint = Blueprint('views_front',__name__)

@views_blueprint.route('/docentes', methods=['GET'])
def show_docentes():
    return render_template('docentesCRUD/docentes.html')