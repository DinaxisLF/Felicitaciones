from flask import Flask
from flask_mysqldb import MySQL
from config import config
from app.email_service.email_sender import EmailSender



db = MySQL()


def page_not_found(error):
    return "<h1>Pagina No Encontrada</h1>" , 404

def init_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config['development'])
    app.register_error_handler(404, page_not_found)

    #Initialize MYSQL
    db.init_app(app)

    #Register Blueprints
    from app.api import docentes_api
    from app.routes.views import views_blueprint
    from app.email_service import email_sender_class
    from app.api.birthday_check import BirthdayChecker
    app.register_blueprint(docentes_api)
    app.register_blueprint(email_sender_class)
    app.register_blueprint(views_blueprint)

 # Verificar cumpleaños al correr run.py
    with app.app_context():
        docentes_cumpleanos = BirthdayChecker.check_birthdays()
        if docentes_cumpleanos:
            email_sender = EmailSender()
            print("Hoy es el cumpleaños de los siguientes docentes:")
            for docente in docentes_cumpleanos:
                print(f"Docente: {docente[0]} {docente[1]}")
                
                subject = "¡Feliz Cumpleaños!"
                body = f"Estimado/a {docente[0]} {docente[1]},\n\n¡Te deseamos un muy feliz cumpleaños!\n\nAtentamente,\nYo."

                email_sender.send_email(docente[2], subject, body)

        else:
            print("Hoy no es el cumpleaños de ningún docente.")

    return app