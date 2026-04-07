# services/user_service.py - Business logic layer for user operations

from sqlalchemy.orm import Session
from queries.users_query import get_user_by_id, get_all_users, get_user_by_email, create_user, update_user
from models.users_model import UserResponse, UserCreate, UserLogin, ForgetPasswordReq, UserUpdate


def get_user_by_id_service(db: Session, user_id: str) -> UserResponse | None:
    """Service function to get a user by ID."""
    return get_user_by_id(db, user_id)


def get_all_users_service(db: Session) -> list[UserResponse]:
    """Service function to get all users."""
    return get_all_users(db)


def signup_user_service(db: Session, user_data: UserCreate) -> UserResponse | dict:
    """Validates if user exists and creates a new user."""
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        return {"error": "User with this email already exists"}
    return create_user(db, user_data)


def login_user_service(db: Session, login_data: UserLogin) -> UserResponse | dict:
    """Authenticates a user by email and password."""
    from db_models.users_db_model import Users
    user = db.query(Users).filter(Users.email == login_data.email).first()

    if not user:
        return {"error": "Invalid email or password"}

    if user.password != login_data.password:
        return {"error": "Invalid email or password"}

    return UserResponse.from_orm(user)


def forget_password_service(db: Session, email_data: ForgetPasswordReq) -> dict:
    """Mocks an email sent logic if user exists."""
    from db_models.users_db_model import Users
    user = db.query(Users).filter(Users.email == email_data.email).first()

    if not user:
        return {"error": "No user found with that email"}

    return {"message": "Password reset link sent to your email successfully"}


def update_user_service(db: Session, user_id: str, user_data: UserUpdate) -> UserResponse | dict:
    """Service function to update user details."""
    update_dict = user_data.model_dump(exclude_unset=True)

    if not update_dict:
        return {"error": "No fields provided for update"}

    result = update_user(db, user_id, update_dict)
    if not result:
        return {"error": "User not found"}
    return result