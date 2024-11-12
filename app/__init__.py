from flask import Flask
from app.routes.canopen_routes import canopen_bp

def create_app():
    app = Flask(__name__)

    app.register_blueprint(canopen_bp, url_prefix='/canopen')

    return app
