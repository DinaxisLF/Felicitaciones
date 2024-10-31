from datetime import date
from app import db 

class BirthdayChecker:
    @staticmethod
    def check_birthdays():
        today = date.today()
        day, month = today.day, today.month
        cursor = db.connection.cursor()
        
        # Check Birthday
        query = """
        SELECT Nombre, Apellido, Correo, ID_docente
        FROM docente
        WHERE DAY(Fecha_de_Nacimiento) = %s
        AND MONTH(Fecha_de_Nacimiento) = %s
        AND ID_docente NOT IN (
        SELECT ID_docente FROM felicitacion WHERE ID_sistema = 
        (SELECT MAX(ID_sistema) FROM sistema WHERE Fecha_de_ejecucion = %s AND Resultado = 1))
        """
        cursor.execute(query, (day, month, today))
        docentes_with_birthday = cursor.fetchall()
        cursor.close()

        return docentes_with_birthday

    #If emails are send then save the execution of the process in the database
    def log_execution(self):
        today = date.today()
        cursor = db.connection.cursor()
        
        # Check if today's execution was already successful
        cursor.execute("SELECT ID_sistema FROM sistema WHERE Fecha_de_ejecucion = %s AND Resultado = 1", (today,))
        result = cursor.fetchone()

        if result:
            id_sistema = result[0]  
            cursor.close()
            return id_sistema, False  
        
        # Insert new execution log if none exists
        cursor.execute("INSERT INTO sistema (Fecha_de_ejecucion, Resultado) VALUES (%s, %s)", (today, 0))
        db.connection.commit()
        id_sistema = cursor.lastrowid
        cursor.close()
    
        
        return id_sistema, True  
    
    def update_execution_status(self, id_sistema, success):
        cursor = db.connection.cursor()
        cursor.execute("UPDATE sistema SET Resultado = %s WHERE ID_sistema = %s", (int(success), id_sistema))
        db.connection.commit()
        cursor.close()

    #Save the pdf link sent by email
    def log_email_sent(self, id_sistema, id_docente, pdf_link):
        cursor = db.connection.cursor()
        cursor.execute("INSERT INTO felicitacion (ID_sistema, ID_docente, PDF) VALUES (%s, %s, %s)", (id_sistema, id_docente, pdf_link))
        db.connection.commit()
        cursor.close()