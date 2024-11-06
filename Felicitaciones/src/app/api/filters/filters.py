from flask import Blueprint, request, jsonify, current_app
from app import db 

# Crear el blueprint
filters_blueprint = Blueprint('filters_blueprint', __name__)

@filters_blueprint.route('/filtrar_docentes', methods=['GET'])
def filtrar_docentes():
    try:
        #para paginacion
        per_page = int(request.args.get('per_page', 4))
        page = int(request.args.get('page', 1))
        offset = (page - 1) * per_page

        query = "SELECT * FROM docente WHERE 1=1"
        params = []

        nombre = request.args.get('nombre', default='')
        estado = request.args.get('estado', default='')
        mes_nacimiento = request.args.get('mesNacimiento', default='')

        if nombre:
            query += " AND Nombre LIKE %s"
            params.append(f"%{nombre}%")
        
        if estado:
            query += " AND Estado = %s"
            params.append(estado)
        
        if mes_nacimiento:
            query += " AND MONTH(Fecha_de_Nacimiento) = %s"
            params.append(mes_nacimiento)

        query += " LIMIT %s OFFSET %s"
        params.extend([per_page, offset])

        cursor = db.connection.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        docentes = [
            {
                'ID_docente': row[0],
                'Nombre': row[1],
                'Apellido': row[2],
                'Fecha_de_Nacimiento': row[3],
                'Correo': row[4],
                'Estado': row[5]
            }
            for row in results
        ]


        count_query = "SELECT COUNT(*) FROM docente WHERE 1=1"
        count_params = []

        if nombre:
            count_query += " AND Nombre LIKE %s"
            count_params.append(f"%{nombre}%")
        
        if estado:
            count_query += " AND Estado = %s"
            count_params.append(estado)
        
        if mes_nacimiento:
            count_query += " AND MONTH(Fecha_de_Nacimiento) = %s"
            count_params.append(mes_nacimiento)

        cursor.execute(count_query, count_params)
        total_docentes = cursor.fetchone()[0]
        total_pages = (total_docentes + per_page - 1) // per_page

        cursor.close()

        return jsonify({
            'teachers': docentes,
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages,
            'total_docentes': total_docentes
        })

    except Exception as e:
        current_app.logger.error(f"Error al ejecutar la consulta de filtrado: {e}")
        return jsonify({"error": "Error al obtener datos de docentes"}), 500
