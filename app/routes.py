from flask import request, jsonify


def register_routes(app):

    @app.route("/")
    def home():
        return jsonify({"message": "API running"}), 200