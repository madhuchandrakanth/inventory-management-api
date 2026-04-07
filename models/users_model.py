# users-model.py - Pydantic models for request/response validation
# These are used for API input/output validation and serialization

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Base user model with common fields
class UserBase(BaseModel):
    user_id: str
    email: str
    full_name: str
    phone: str

# Model for creating a new user (password required)
class UserCreate(UserBase):
    password: str

# Model for user response (excludes password for security)
class UserResponse(UserBase):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # Enable ORM mode to work with SQLAlchemy models
    class Config:
        from_attributes = True

# Model for user login
class UserLogin(BaseModel):
    email: str
    password: str

# Model for forget password request
class ForgetPasswordReq(BaseModel):
    email: str

# Model for updating user details (all fields optional for partial update)
class UserUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None