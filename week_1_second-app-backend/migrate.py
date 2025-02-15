# This script runs migrations directly without invoke.
from app import app
from db import init_db

with app.app_context():
    init_db()
    print("Database migrated successfully.")
