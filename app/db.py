import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import time
from .models import Base

# Create engine for maintenance database (postgres)
MAINTENANCE_DB_URL = "postgresql://postgres:1234@postgres:5432/postgres"
maint_engine = create_engine(MAINTENANCE_DB_URL)


def ensure_database_exists():
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


# Create tables in chatlog database
def create_tables():
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