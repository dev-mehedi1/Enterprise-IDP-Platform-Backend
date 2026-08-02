from beanie import Document
from pydantic import Field, EmailStr
from typing import List, Optional
from datetime import datetime, timezone

class Role(Document):
    name: str = Field(unique=True)
    permissions: List[str] = []
    
    class Settings:
        name = "roles"

class User(Document):
    email: EmailStr = Field(unique=True)
    hashed_password: str
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False
    roles: List[str] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Settings:
        name = "users"
