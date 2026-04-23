from flask import Blueprint, request, jsonify, session
from app.extensions import db  
from app.models.user import User
from app.extensions import bcrypt

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/signup", methods=["POST"])
def signup():

    data = request.get_json()

    # Input validation
    required = ["username", "email", "password"]
    missing = [field for field in required if not data or field not in data or not data[field]]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    # Check for existing username or email
    existing = User.query.filter(
        (User.username == data["username"]) | (User.email == data["email"])
    ).first()

    if existing:
        if existing.username == data["username"]:
            return jsonify({"error": "Username already taken"}), 409
        return jsonify({"error": "Email already registered"}), 409

    hashed = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

    user = User(
        username=data["username"],
        email=data["email"],
        password_hash=hashed
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User created",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    # Input validation
    required = ["username", "password"]
    missing = [field for field in required if not data or field not in data or not data[field]]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    user = User.query.filter_by(username=data["username"]).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not bcrypt.check_password_hash(user.password_hash, data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    session["user_id"] = user.id

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user.id,
            "username": user.username,
        }
    }), 200

@auth_bp.route("/logout", methods=["POST"])
def logout():

    session.pop("user_id", None)

    return jsonify({"message": "Logged out successfully"}), 200