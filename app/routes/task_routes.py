from flask import Blueprint, request, jsonify, session
from app.extensions import db  
from app.models.task import Task

task_bp = Blueprint("task_bp", __name__)


# CREATE TASK
@task_bp.route("/tasks", methods=["POST"])
def create_task():

    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()

    # Input validation
    if not data or not data.get("title"):
        return jsonify({"error": "Missing required field: title"}), 400

    task = Task(
        title=data["title"],
        description=data.get("description"),
        user_id=user_id
    )

    db.session.add(task)
    db.session.commit()

    return jsonify({
        "message": "Task created",
        "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed
        }
    }), 201


# GET TASKS
@task_bp.route("/tasks", methods=["GET"])
def get_tasks():

    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    tasks = Task.query.filter_by(user_id=user_id).all()

    return jsonify([
        {
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "completed": t.completed
        } for t in tasks
    ]), 200


# UPDATE TASK
@task_bp.route("/tasks/<int:id>", methods=["PATCH"])
def update_task(id):

    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    task = Task.query.filter_by(id=id, user_id=user_id).first()

    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()

    # Input validation
    if not data:
        return jsonify({"error": "No data provided"}), 400

    if "title" in data and not data["title"]:
        return jsonify({"error": "Title cannot be empty"}), 400

    if "title" in data:
        task.title = data["title"]

    if "description" in data:
        task.description = data["description"]