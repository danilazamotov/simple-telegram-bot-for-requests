import os
from dotenv import load_dotenv
from database.DatabaseConfig import DatabaseConfig


def requests_initialize_database():
    load_dotenv()
    requests_database_path = os.getenv("DATABASE_PATH")
    if requests_database_path is None:
        raise ValueError("DATABASE_PATH is not set in the environment variables.")

    config_db = DatabaseConfig(requests_database_path)
    config_db.initialize()

    if not os.path.exists(requests_database_path):
        raise FileNotFoundError(f"Database file not found at: {requests_database_path}")

    return config_db
