from flask import jsonify, request
from app.api import docentes_api
from datetime import datetime, date
from werkzeug.utils import secure_filename
from flask_login import login_required
import pandas as pd
import os
import tempfile
import re




@docentes_api.route('/api/docentes', methods=['GET'])
@login_required
def list():
    try:
        # Get filter parameters from the request
        nombre = request.args.get('nombre', '')
        estado = request.args.get('estado', '')
        mes_nacimiento = request.args.get('mesNacimiento', '')

        per_page = int(request.args.get('per_page', 4))
        page = int(request.args.get('page', 1))
        offset = (page - 1) * per_page

        # Start the query with basic conditions
        query = "SELECT * FROM docente WHERE 1=1"
        params = []

        # Filter by name
        if nombre:
            query += " AND (Nombre LIKE %s OR Apellido LIKE %s)"
            params.extend([f'%{nombre}%', f'%{nombre}%'])

        # Filter by state
        if estado:
            query += " AND Estado = %s"
            params.append(estado)

        # Filter by month of birth
        if mes_nacimiento:
            query += " AND EXTRACT(MONTH FROM Fecha_de_Nacimiento) = %s"
            params.append(mes_nacimiento)

        # Apply pagination (limit and offset)
        query += " LIMIT %s OFFSET %s"
        params.extend([per_page, offset])

        # Execute the query with parameters
        from app import db
        cursor = db.connection.cursor()
        cursor.execute(query, tuple(params))  # Ensure the parameters are passed as a tuple
        response = cursor.fetchall()

        teachers = [
            {
                'ID_docente': teacher[0],
                'Nombre': teacher[1],
                'Apellido': teacher[2],
                'Fecha_de_Nacimiento': teacher[3].strftime("%d-%m-%Y"),
                'Correo': teacher[4],
                'Estado': teacher[5]
            }
            for teacher in response
        ]

        # Count total rows after filtering
        count_query = "SELECT COUNT(*) FROM docente WHERE 1=1"
        count_params = []

        # Count by name
        if nombre:
            count_query += " AND (Nombre LIKE %s OR Apellido LIKE %s)"
            count_params.extend([f'%{nombre}%', f'%{nombre}%'])

        # Count by state
        if estado:
            count_query += " AND Estado = %s"
            count_params.append(estado)

        # Count by month of birth
        if mes_nacimiento:
            count_query += " AND EXTRACT(MONTH FROM Fecha_de_Nacimiento) = %s"
            count_params.append(mes_nacimiento)

        # Execute the count query
        cursor.execute(count_query, tuple(count_params))
        total_docentes = cursor.fetchone()[0]
        total_pages = (total_docentes + per_page - 1) // per_page

        # Return the filtered data and pagination info
        return jsonify({
            'teachers': teachers,
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages,
            'total_docentes': total_docentes
        }), 200

    except Exception as ex:
        return jsonify({'message': "Error in the query"}), 500


@docentes_api.route('/api/docentes/<id>', methods=['GET'])
@login_required
def consult(id):
    try:
        from app import db
        cursor = db.connection.cursor()
        query = "SELECT * FROM docente where ID_docente = '{0}'".format(id)
        cursor.execute(query)
        response = cursor.fetchone()
        
        if response != None:
            data={'ID_docente':response[0],'Nombre':response[1], 'Apellido':response[2], 
                'Fecha_de_Nacimiento':response[3], 'Correo':response[4], 'Estado':response[5]}
            return jsonify({'docentes_api':data, 'message': "Consulta Realizada (docentes_api)"})
        else:
            return jsonify({'message':"Docente no encontrado"})
    except Exception as ex:
        return jsonify({'message':"Error en la consulta"})


@docentes_api.route('/api/docentes/<id>', methods = ["PUT"])
@login_required
def actulizar_docente(id):
    try:
        from app import db
        cursor = db.connection.cursor()
        query = """UPDATE docente SET Nombre = '{0}' , Apellido = '{1}', Fecha_de_Nacimiento = '{2}', 
        Correo = '{3}', Estado  = '{4}' WHERE ID_docente = '{5}'""".format(request.json['Nombre'], request.json['Apellido']
                                                            ,request.json['Fecha_de_Nacimiento']
                                                            , request.json['Correo']
                                                            ,request.json['Estado'], id)
        cursor.execute(query)
        db.connection.commit()
        return jsonify({'message': "Docente Actualizado.", 'exito': True})
    except Exception as ex:
        return jsonify({'message':"Docente no encontrado",'exito': False})


@docentes_api.route('/api/docentes/<id>', methods = ['DELETE'])
@login_required
def eliminar_docente(id):
    try:
        from app import db
        cursor = db.connection.cursor()
        query = "DELETE FROM docente WHERE ID_docente = '{0}'".format(id)
        cursor.execute(query)
        db.connection.commit()
        return jsonify({'message': "Docente eliminado", 'exito': True})
    except Exception as ex:
        return jsonify({'message':"Docente no encontrado",'exito': False})
    


#Allow Excel and GoogleSheets
ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




@docentes_api.route('/api/docentes', methods=['POST'])
@login_required
def registrar_docente():
    try:
        import app
        if 'file' not in request.files:
            return jsonify({'message': 'No file part', 'exito': False}), 400
        file = request.files['file']

        if file.filename == '':
            return jsonify({'message': 'No selected file', 'exito': False}), 400

        if file and allowed_file(file.filename):
            # Secure the filename
            filename = secure_filename(file.filename)

            UPLOAD_FOLDER = 'uploads/temp/'
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)

            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Save the file temporarily
            file.save(filepath)

            # Process the file with pandas
            df = pd.read_excel(filepath)

            # Here you can validate the data before processing further, as shown in the earlier steps

            # Process the file (for example, inserting records into your database)
            for index, row in df.iterrows():
                # Example data insertion, adjust as per your logic
                nombre = row['Nombre']
                apellido = row['Apellido']
                fecha_nacimiento = row['Fecha_de_Nacimiento']
                correo = row['Correo']
                estado = row['Estado']
                from app import db
                # Insert the data into your database
                cursor = db.connection.cursor()
                query = """INSERT INTO docente (Nombre, Apellido, Fecha_de_Nacimiento, Correo, Estado) 
                        VALUES (%s, %s, %s, %s, %s)"""
                cursor.execute(query, (nombre, apellido, fecha_nacimiento, correo, estado))
                db.connection.commit()

            # Optionally, remove the file after processing
            os.remove(filepath)

            return jsonify({'message': 'Docentes uploaded and saved successfully!', 'exito': True})

        else:
            return jsonify({'message': 'Invalid file type. Please upload an Excel file.', 'exito': False}), 400

    except Exception as ex:
        print (ex)
        return jsonify({'message': f'Error: {str(ex)}', 'exito': False}), 500