from datetime import date
from app import db 

class BirthdayChecker:
    @staticmethod
    def check_birthdays():
        today = date.today()
        day = today.day
        month = today.month

        cursor = db.connection.cursor()
        
        # query verificar cumpleaños
        query = """
        SELECT Nombre, Apellido 
        FROM docente 
        WHERE DAY(Fecha_de_Nacimiento) = %s AND MONTH(Fecha_de_Nacimiento) = %s
        """
        cursor.execute(query, (day, month))
        docentes_with_birthday = cursor.fetchall()

        cursor.close()

        return docentes_with_birthday
