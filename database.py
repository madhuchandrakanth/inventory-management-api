# database.py - Database configuration and session management

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Load environment variables from .env file
load_dotenv()

# Database URL from environment variable with fallback
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:12345678@localhost:5432/inventory-dev"
)

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Modern declarative base using SQLAlchemy 2.0 style
class Base(DeclarativeBase):
    pass


def get_db():
    """Dependency to get a database session for each request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()