from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    """
    Schema for user creation request.

    Attributes:
        email (EmailStr): The user's email address.
        password (str): The user's password.
    """
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    """
    Schema for user login request.

    Attributes:
        email (EmailStr): The user's email address.
        password (str): The user's password.
    """
    email: EmailStr
    password: str

class UserInDB(BaseModel):
    """
    Schema for user information stored in the database.

    Attributes:
        id (int): The user's unique identifier.
        email (EmailStr): The user's email address.
        is_active (bool): Whether the user account is active.

    Config:
        orm_mode = True: Allows the Pydantic model to read the data even if it's not a dict, but an ORM model.
    """
    id: int
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True