from flask import Flask


def init_app():
    app = Flask(__name__)

    # Configuração do app
    app.secret_key = "vitorvitoriaeyaramariaauvesdacosta"

    # Database
    # from .database import DBConnectionHendler
    # from .database import Base

    # db_connection = DBConnectionHendler()
    # engine = db_connection.get_engine()

    with app.app_context(): 

         # Aplicativo inicial
        from .blueprints import initial_app

        app.register_blueprint(initial_app)

         # Aplicativo apostar
        from .blueprints import apostar_app

        app.register_blueprint(apostar_app)

        return app