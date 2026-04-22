from flask import Flask
from .extensions import db, migrate, bcrypt

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "dev-secret-key"

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    from . import models
    from .routes import register_routes
    register_routes(app)

    return app