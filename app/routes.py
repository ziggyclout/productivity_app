from flask import request, jsonify, session
from .models import db, User

def register_routes(app):

    # -------------------------
    # HOME
    # -------------------------
    @app.route("/")
    def home():
        return jsonify({"message": "API running"}), 200


    # -------------------------
    # SIGNUP
    # -------------------------
    @app.route("/signup", methods=["POST"])
    def signup():
        data = request.get_json()

        if not data:
            return jsonify({"error": "Missing JSON"}), 400

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            return jsonify({"error": "All fields required"}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Username exists"}), 409

        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email exists"}), 409

        user = User(username=username, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "User created"}), 201


    # -------------------------
    # LOGIN
    # -------------------------
    @app.route("/login", methods=["POST"])
    def login():
        data = request.get_json()

        if not data:
            return jsonify({"error": "Missing JSON"}), 400

        username = data.get("username")
        password = data.get("password")

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            return jsonify({"error": "Invalid credentials"}), 401

        session["user_id"] = user.id

        return jsonify({"message": "Logged in"}), 200


    # -------------------------
    # ME (SESSION CHECK)
    # -------------------------
    @app.route("/me", methods=["GET"])
    def me():
        user_id = session.get("user_id")

        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401

        user = User.query.get(user_id)

        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email
        }), 200


    # -------------------------
    # LOGOUT
    # -------------------------
    @app.route("/logout", methods=["DELETE"])
    def logout():
        session.pop("user_id", None)
        return jsonify({"message": "Logged out"}), 200