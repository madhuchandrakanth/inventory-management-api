# queries/users_query.py - Database query functions using SQLAlchemy
# This file contains functions to interact with the users table

from sqlalchemy.orm import Session
from db_models.users_db_model import Users
from models.users_model import UserCreate, UserResponse


def get_user_by_id(db: Session, user_id: str) -> UserResponse | None:
    """
    Fetch a single user by their user_id.

    Args:
        db: SQLAlchemy database session
        user_id: The unique identifier of the user

    Returns:
        UserResponse object if found, None if not found
    """
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if user:
        return UserResponse.from_orm(user)
    return None


def get_all_users(db: Session) -> list[UserResponse]:
    """
    Fetch all users from the database.

    Args:
        db: SQLAlchemy database session

    Returns:
        List of UserResponse objects
    """
    users = db.query(Users).all()
    return [UserResponse.from_orm(user) for user in users]


def create_user(db: Session, user: UserCreate) -> UserResponse:
    """
    Create a new user in the database.

    Args:
        db: SQLAlchemy database session
        user: UserCreate object with user data

    Returns:
        UserResponse object of the created user
    """
    db_user = Users(
        user_id=user.user_id,
        email=user.email,
        password=user.password,
        full_name=user.full_name,
        phone=user.phone
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return UserResponse.from_orm(db_user)


def get_user_by_email(db: Session, email: str) -> UserResponse | None:
    """
    Fetch a user by their email address.

    Args:
        db: SQLAlchemy database session
        email: The email address to search for

    Returns:
        UserResponse object if found, None if not found
    """
    user = db.query(Users).filter(Users.email == email).first()
    if user:
        return UserResponse.from_orm(user)
    return None


def update_user(db: Session, user_id: str, user_data: dict) -> UserResponse | None:
    """
    Update user information.

    Args:
        db: SQLAlchemy database session
        user_id: The user to update
        user_data: Dictionary of fields to update

    Returns:
        Updated UserResponse object if successful, None if user not found
    """
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if not user:
        return None

    for key, value in user_data.items():
        if hasattr(user, key):
            setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return UserResponse.from_orm(user)


def delete_user(db: Session, user_id: str) -> bool:
    """
    Delete a user from the database.

    Args:
        db: SQLAlchemy database session
        user_id: The user to delete

    Returns:
        True if deleted, False if user not found
    """
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if not user:
        return False

    db.delete(user)
    db.commit()
    return True
