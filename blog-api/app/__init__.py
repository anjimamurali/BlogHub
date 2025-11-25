from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from .config import Config
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS for all routes with simpler configuration
    CORS(app, origins="*")
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Import and register blueprints
    from .routes import bp as api_bp
    print(f"Imported blueprint: {api_bp}")
    print("Blueprint imported successfully")
    app.register_blueprint(api_bp, url_prefix='/api')
    print("Blueprint registered successfully")
    
    # Import models to ensure they are registered with SQLAlchemy
    from . import models
    
    return app
