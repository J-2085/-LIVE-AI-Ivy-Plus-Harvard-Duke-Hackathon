from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)


    from backend_ibm.blueprints.core.routes import core
    from backend_ibm.blueprints.ai.routes import aiRoute


    app.register_blueprint(core, url_prefix='/')
    app.register_blueprint(aiRoute, url_prefix='/ai')

    return app