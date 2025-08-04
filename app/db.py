import os
import time

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

from .models import Base

# Create engine for maintenance database (postgres)
MAINTENANCE_DB_URL = "postgresql://postgres:1234@postgres:5432/postgres"
maint_engine = create_engine(MAINTENANCE_DB_URL)


def ensure_database_exists():
    """
    Ensures that the required PostgreSQL databases exist.

    This function connects to the maintenance database and checks if the
    'chatlog' and 'legalclauseanalyzer_metadata' databases exist. If not,
    it creates them. It retries the connection and creation process up to
    MAX_RETRIES times, with a delay of WAIT_SECONDS between attempts.

    Returns:
        bool: True if the databases exist or were created successfully, False otherwise.
    """
    MAX_RETRIES = 5
    WAIT_SECONDS = 3

    for attempt in range(MAX_RETRIES):
        try:
            with maint_engine.connect() as conn:
                # Create databases if they don't exist
                for db_name in ["chatlog", "legalclauseanalyzer_metadata"]:
                    result = conn.execute(
                        text("SELECT 1 FROM pg_database WHERE datname = :dbname"),
                        {"dbname": db_name}
                    )
                    if not result.scalar():
                        conn.execute(text(f"CREATE DATABASE {db_name}"))
                        print(f"Created database: {db_name}")
                conn.commit()
            return True
        except OperationalError as e:
            print(f"Database connection failed ({attempt + 1}/{MAX_RETRIES}): {e}")
            time.sleep(WAIT_SECONDS)
    print("Failed to create databases after retries")
    return False


# Ensure databases exist before proceeding
ensure_database_exists()

# Now create engine for application database
DATABASE_URL = os.getenv("CHATLOG_DATABASE")
engine = create_engine(DATABASE_URL)


def create_tables():
    """
    Creates all tables defined in the SQLAlchemy Base metadata in the target database.

    This function connects to the application database (as defined by DATABASE_URL)
    and attempts to create the tables using SQLAlchemy's `create_all()` method.
    It retries the operation up to MAX_RETRIES times in case of connection issues.

    Returns:
        bool: True if the tables were created successfully, False otherwise.
    """
    MAX_RETRIES = 5
    WAIT_SECONDS = 3

    for attempt in range(MAX_RETRIES):
        try:
            Base.metadata.create_all(bind=engine)
            print("Database tables created successfully")
            return True
        except OperationalError as e:
            print(f"Table creation failed ({attempt + 1}/{MAX_RETRIES}): {e}")
            time.sleep(WAIT_SECONDS)
    print("Failed to create tables after retries")
    return False


create_tables()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)