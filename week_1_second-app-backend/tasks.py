from invoke import task
from app import app
from db import init_db

@task
def init_db_task(c):
    """Initialize and migrate the database for the Extended Chinese Learning App."""
    with app.app_context():
        init_db()
    print("Database initialized and migrated successfully.")