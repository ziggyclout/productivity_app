from .extensions import db, bcrypt


# -------------------------
# USER MODEL (AUTH)
# -------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    tasks = db.relationship("Task", backref="user", lazy=True)

    def set_password(self, password):
        if not password or len(password) < 4:
            raise ValueError("Password too short")
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


# -------------------------
# TASK MODEL (RESOURCE)
# -------------------------
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)