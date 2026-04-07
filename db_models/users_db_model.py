# users-db-model.py - SQLAlchemy model for Users table
# This defines the database table structure using SQLAlchemy ORM

from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.sql import func
from database import Base  # Import Base from our database configuration

class Users(Base):
    # Define the table name explicitly
    __tablename__ = "users"

    # Define columns with their types and constraints
    # user_id is the primary key, unique and not null
    user_id = Column(String(255), primary_key=True, unique=True, nullable=False)

    # email is unique and not null
    email = Column(String(255), unique=True, nullable=False)

    # password stored as text (should be hashed in real app)
    password = Column(Text, nullable=False)

    # full_name instead of just name
    full_name = Column(String(100), nullable=False)

    # phone number
    phone = Column(String(10), nullable=False)

    # created_at with default timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # updated_at with default and onupdate timestamp
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())