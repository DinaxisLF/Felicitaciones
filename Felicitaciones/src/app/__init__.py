from flask import Flask
from flask_mysqldb import MySQL
from config import config


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
    app.register_blueprint(docentes_api)
    app.register_blueprint(email_sender_class)
    app.register_blueprint(views_blueprint)

    return app