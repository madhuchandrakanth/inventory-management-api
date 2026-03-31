from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Users(Base):
    user_id: str
    name: str
    email: str
    password: str
    role: str
    created_at: str
    updated_at: str