#Flask Application Setup
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

def create_app(config_class='config'):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    
    # Register blueprints
    from app.controllers.application_controller import application_bp
    from app.controllers.certificate_controller import certificate_bp
    from app.controllers.pdf_controller import pdf_bp
    
    app.register_blueprint(application_bp)
    app.register_blueprint(certificate_bp)
    app.register_blueprint(pdf_bp)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app