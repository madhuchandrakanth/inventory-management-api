from pydantic import BaseModel

class Users(BaseModel):
    user_id: str
    name: str
    email: str
    password: str
    role: str
    created_at: str
    updated_at: str