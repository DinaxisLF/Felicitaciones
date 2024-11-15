from flask import Flask, render_template
from flask_mysqldb import MySQL
from config import config
from flask_login import LoginManager
from app.birthdayGreeting.greetingMaker import greeting_maker
from app.api.login import User
from dotenv import load_dotenv
import os 
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime


login_manager = LoginManager()
db = MySQL()


def page_not_found(error):
    return render_template('auth/notfound.html'), 404

def init_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config['development'])
    app.register_error_handler(404, page_not_found)

    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return response

    load_dotenv()
    app.secret_key = os.getenv("SECRET_KEY")

    #Initialize MYSQL
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'views_front.home'  # Set default login route
    



    #Register Blueprints
    from app.api import docentes_api
    from app.routes.views import views_blueprint
    app.register_blueprint(docentes_api)
    app.register_blueprint(views_blueprint)

    #APScheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(greeting_task, 'cron', hour=19, minute=5, second=35, misfire_grace_time=3600)
    scheduler.start()

    return app

def greeting_task():
    from app import init_app

    app = init_app()

    with app.app_context():
        from app.birthdayGreeting.birthday_check import BirthdayChecker
        birthday = BirthdayChecker()

        id_sistema, new_execution = birthday.log_execution()

        if not new_execution:
            print("Por hoy ya no hay correos por enviar")

        else:
            docentes_cumpleanos = birthday.check_birthdays()

            if docentes_cumpleanos:    
                success = True
                print("Hoy es el cumpleaños de los siguientes docentes:")
                for docente in docentes_cumpleanos:

                    subject = "¡Feliz Cumpleaños!"
                    body = f"Estimado/a {docente[0]} {docente[1]},\n\n¡Te deseamos un muy feliz cumpleaños!\n\nAtentamente,\nMtro. Jose Alfredo Peña Ramos"
                    pdf = greeting_maker(docente,subject, body)


                    print(f"Docente: {docente[0]} {docente[1]}")
                        
                    try:
                        birthday.log_email_sent(id_sistema, docente[3], pdf)
                    except Exception as e:
                        print(f"Error al enviar email al docente: {docente[2]}: {e}")
                        success = False


                birthday.update_execution_status(id_sistema, success)

            else:
                print("Hoy no es el cumpleaños de ningún docente.")

    

@login_manager.user_loader
def load_user(user_id):
        cursor = db.connection.cursor()
        cursor.execute("SELECT ID_administrador, Correo FROM administrador WHERE ID_administrador = %s", (user_id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return User(id=result[0], email=result[1])
        return None