from app import create_app
from app.extensions import db, bcrypt
from app.models.user import User
from app.models.task import Task

app = create_app()

with app.app_context():

    # Clear existing data
    print("Clearing existing data...")
    Task.query.delete()
    User.query.delete()
    db.session.commit()

    # Create users
    print("Seeding users...")
    users = [
        User(
            username="walter_white",
            email="walter@white.com",
            password_hash=bcrypt.generate_password_hash("password123").decode("utf-8")
        ),
        User(
            username="jesse_pinkman",
            email="jesse@pinkman.com",
            password_hash=bcrypt.generate_password_hash("password123").decode("utf-8")
        ),
        User(
            username="saul_goodman",
            email="saul@goodman.com",
            password_hash=bcrypt.generate_password_hash("password123").decode("utf-8")
        ),
    ]

    db.session.add_all(users)
    db.session.commit()

    # Create tasks
    print("Seeding tasks...")
    tasks = [
        Task(title="Buy lab equipment", description="Get everything needed for the lab", completed=False, user_id=users[0].id),
        Task(title="Check on the product", description="Make sure quality is consistent", completed=True, user_id=users[0].id),
        Task(title="Call Saul", description="Need legal advice ASAP", completed=False, user_id=users[0].id),

        Task(title="Pick up the money", description="From the drop spot on Central", completed=False, user_id=users[1].id),
        Task(title="Find a new buyer", description="Expand the distribution network", completed=False, user_id=users[1].id),

        Task(title="File the paperwork", description="LLC formation for the car wash", completed=True, user_id=users[2].id),
        Task(title="Meet with the client", description="New client consultation at 3pm", completed=False, user_id=users[2].id),
        Task(title="Prepare the defense", description="Review case files before court", completed=False, user_id=users[2].id),
    ]

    db.session.add_all(tasks)
    db.session.commit()

    print("Done seeding!")