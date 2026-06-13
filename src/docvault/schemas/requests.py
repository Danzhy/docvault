from pydantic import BaseModel, EmailStr, Field, field_validator
import re

class User(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=40)

    @field_validator('password')
    @classmethod
    def validate_password(cls, password: str) -> str:
        
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must have at least 1 digit")
        
        if not any(char.islower() for char in password):
            raise ValueError("Password must have at least 1 lowercase letter")
        
        if not any(char.isupper() for char in password):
            raise ValueError("Password must have at least 1 uppercase letter")
        
        special = "!@#$%^&*()-_"
        special_re = f"[{re.escape(special)}]"
        if not re.search(special_re, password):
            raise ValueError("Password must have at least 1 special character")

        breakpoint()
        return password