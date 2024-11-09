from flask import Flask
from flask_mysqldb import MySQL
from config import config
from app.email_service.email_sender import EmailSender
from app.birthdayGreeting.greetingMaker import greeting_maker
from app.api.login.login import login_blueprint



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
    from app.api.filters.filters import filters_blueprint
    app.register_blueprint(docentes_api)
    app.register_blueprint(email_sender_class)
    app.register_blueprint(views_blueprint)
    app.register_blueprint(filters_blueprint)
    app.register_blueprint(login_blueprint, url_prefix='/api')

    from app.birthdayGreeting.birthday_check import BirthdayChecker
    

    #Check if its someone birthday and then send an email greeting
    with app.app_context():
        
        birthday = BirthdayChecker()
        email_sender = EmailSender()

        id_sistema, new_execution = birthday.log_execution()

        if not new_execution:
            print("Por hoy ya no hay correos por enviar")

        else:
            docentes_cumpleanos = birthday.check_birthdays()

            if docentes_cumpleanos:    
                success = True
                print("Hoy es el cumpleaños de los siguientes docentes:")
                for docente in docentes_cumpleanos:

                    pdf = greeting_maker(docente)

                    print(f"Docente: {docente[0]} {docente[1]}")
                    
                    subject = "¡Feliz Cumpleaños!"
                    body = f"Estimado/a {docente[0]} {docente[1]},\n\n¡Te deseamos un muy feliz cumpleaños!\n\nAtentamente,\nYo."
                    
                    try:
                        email_sender.send_email(docente[2], subject, body, pdf)
                        birthday.log_email_sent(id_sistema, docente[3], "PDF")
                    except Exception as e:
                        print(f"Error al enviar email al docente: {docente[2]}: {e}")
                        success = False


                birthday.update_execution_status(id_sistema, success)

            else:
                print("Hoy no es el cumpleaños de ningún docente.")

    return app