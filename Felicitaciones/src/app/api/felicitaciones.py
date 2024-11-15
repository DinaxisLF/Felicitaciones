from . import docentes_api
from flask import jsonify, request

@docentes_api.route('/api/felicitaciones')
def felicitaciones_list():
    try:
        # Get filter parameters from query string
        id_docente = request.args.get('idDocente', '')
        fecha = request.args.get('fecha', '')

        per_page = int(request.args.get('per_page', 4))  # Number of items per page
        page = int(request.args.get('page', 1))  # Current page
        offset = (page - 1) * per_page

        from app import db
        cursor = db.connection.cursor()

        # Base SQL query
        query = """
        SELECT 
            f.ID_felicitacion, 
            CONCAT(d.Nombre, ' ', d.Apellido) AS Docente, 
            f.PDF, 
            s.Fecha_de_ejecucion, 
            s.ID_sistema
        FROM 
            felicitacion f
        JOIN 
            sistema s ON f.ID_sistema = s.ID_sistema
        JOIN 
            docente d ON f.ID_docente = d.ID_docente
        WHERE 1=1
        """
        params = []

        # Filter by docente name (idDocente)
        if id_docente:
            query += " AND CONCAT(d.Nombre, ' ', d.Apellido) LIKE %s"
            params.append('%' + id_docente + '%')  # Using LIKE for partial matching

        # Filter by fecha (exact date)
        if fecha:
            query += " AND DATE(s.Fecha_de_ejecucion) = %s"
            params.append(fecha)  # fecha is expected in YYYY-MM-DD format

        # Adding pagination (LIMIT and OFFSET)
        query += " LIMIT %s OFFSET %s"
        params.append(per_page)
        params.append(offset)

        # Execute the query with parameters
        cursor.execute(query, tuple(params))
        response = cursor.fetchall()


        felicitaciones = [
            {
                'ID_felicitacion': felicitacion[0],
                'Docente': felicitacion[1],
                'PDF': felicitacion[2],
                'Fecha_de_ejecucion': felicitacion[3].strftime("%d-%m-%Y"),
                'ID_sistema': felicitacion[4]
            }
            for felicitacion in response
        ]

        # Get the total count of rows for pagination
        cursor.execute("SELECT COUNT(*) FROM felicitacion")
        total_felicitaciones = cursor.fetchone()[0]
        total_pages = (total_felicitaciones + per_page - 1) // per_page

        # Return the filtered data with pagination info
        return jsonify({
            'felicitaciones': felicitaciones,
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages,
            'total_felicitaciones': total_felicitaciones
        }), 200

    except Exception as ex:
        return jsonify({'message': "Error en la consulta"}), 500