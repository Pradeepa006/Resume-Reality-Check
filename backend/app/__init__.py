from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import logging

# Shared extensions
db = SQLAlchemy()
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"], storage_uri="memory://")


def create_app():
    """Application factory."""
    app = Flask(__name__)

    # ------------------------------------------------------------------
    # Config
    # ------------------------------------------------------------------
    from config import Config
    app.config.from_object(Config)

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s: %(message)s'
    )

    # ------------------------------------------------------------------
    # Upload folder
    # ------------------------------------------------------------------
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # ------------------------------------------------------------------
    # Extensions
    # ------------------------------------------------------------------
    db.init_app(app)
    limiter.init_app(app)
    CORS(app, origins=app.config.get('CORS_ORIGINS', ['*']), supports_credentials=True)

    # ------------------------------------------------------------------
    # Blueprints
    # ------------------------------------------------------------------
    from app.routes.upload import upload_bp
    from app.routes.analyze import analyze_bp
    from app.routes.history import history_bp

    app.register_blueprint(upload_bp)
    app.register_blueprint(analyze_bp)
    app.register_blueprint(history_bp)

    # ------------------------------------------------------------------
    # Database
    # ------------------------------------------------------------------
    with app.app_context():
        db.create_all()

    return app
