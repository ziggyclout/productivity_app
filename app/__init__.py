from flask import Flask, jsonify
from app.extensions import db, bcrypt, migrate
from app.routes.auth_routes import auth_bp
from app.routes.task_routes import task_bp

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SECRET_KEY"] = "secret-key"

    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    from app.models.user import User
    from app.models.task import Task

    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"error": "Method not allowed"}), 405

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"error": "Internal server error"}), 500

    return app