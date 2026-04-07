# controller/users_controller.py - Controller layer for user endpoints

from sqlalchemy.orm import Session
from services.user_service import (
    get_user_by_id_service,
    get_all_users_service,
    signup_user_service,
    login_user_service,
    forget_password_service,
    update_user_service,
)
from models.users_model import UserResponse, UserCreate, UserLogin, ForgetPasswordReq, UserUpdate
from typing import List
from fastapi import HTTPException


def fetch_user_by_id(user_id: str, db: Session) -> UserResponse | dict:
    """Controller function to fetch a user by ID."""
    user = get_user_by_id_service(db, user_id)
    if user:
        return user
    return {"error": "User not found", "user_id": user_id}


def fetch_users_data(db: Session) -> List[UserResponse]:
    """Controller function to fetch all users."""
    return get_all_users_service(db)


def handle_signup(user_data: UserCreate, db: Session) -> UserResponse:
    """Controller function to handle user registration."""
    result = signup_user_service(db, user_data)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


def handle_login(login_data: UserLogin, db: Session) -> UserResponse:
    """Controller function to handle user login."""
    result = login_user_service(db, login_data)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=401, detail=result["error"])
    return result


def handle_forget_password(email_data: ForgetPasswordReq, db: Session) -> dict:
    """Controller function to handle mock password reset."""
    result = forget_password_service(db, email_data)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


def handle_update_user(user_id: str, user_data: UserUpdate, db: Session) -> UserResponse:
    """Controller function to update user details."""
    result = update_user_service(db, user_id, user_data)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
