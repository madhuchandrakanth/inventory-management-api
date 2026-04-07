# routes/users_routes.py - API routes for user endpoints

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from controller.users_controller import (
    fetch_user_by_id,
    fetch_users_data,
    handle_signup,
    handle_login,
    handle_forget_password,
    handle_update_user,
)
from models.users_model import UserCreate, UserLogin, ForgetPasswordReq, UserUpdate
from database import get_db

# Create a dedicated router for Users
user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.get("/")
def get_users_data(db: Session = Depends(get_db)):
    """GET /users - Fetch all users"""
    return fetch_users_data(db)


@user_router.post("/signup")
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """POST /users/signup - Registers a new user"""
    return handle_signup(user_data, db)


@user_router.post("/login")
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """POST /users/login - Authenticates a user"""
    return handle_login(login_data, db)


@user_router.post("/forget-password")
def forget_password(email_data: ForgetPasswordReq, db: Session = Depends(get_db)):
    """POST /users/forget-password - Sends mock password recovery email"""
    return handle_forget_password(email_data, db)


@user_router.get("/{user_id}")
def get_user_by_id(user_id: str, db: Session = Depends(get_db)):
    """GET /users/{user_id} - Fetch a specific user by ID"""
    result = fetch_user_by_id(user_id, db)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@user_router.put("/{user_id}")
def update_user(user_id: str, user_data: UserUpdate, db: Session = Depends(get_db)):
    """PUT /users/{user_id} - Update user details"""
    return handle_update_user(user_id, user_data, db)
