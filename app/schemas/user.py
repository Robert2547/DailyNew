from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    """
    Schema for user creation request.

    This schema defines the input data structure for creating a new user account. It includes the necessary fields such as email and password.

    Attributes:
        email (EmailStr): The user's email address.
        password (str): The user's password.
    """
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    """
    Schema for user login request.

    This schema defines the input data structure for user login. It includes the necessary fields such as email and password.

    Attributes:
        email (EmailStr): The user's email address.
        password (str): The user's password.
    """
    email: EmailStr
    password: str

class UserInDB(BaseModel):
    """
    Schema for user information stored in the database.

    This schema defines the data structure for a user object as it is stored in the database. It includes the user's unique identifier, email, and whether the account is active.

    Attributes:
        id (int): The user's unique identifier.
        email (EmailStr): The user's email address.
        is_active (bool): Whether the user account is active.

    Config:
        orm_mode = True: Allows the Pydantic model to read the data even if it's not a dict, but an ORM model.
        from_attributes = True: Tells Pydantic to use the attributes of the SQLAlchemy model directly when creating the Pydantic model instance using the `from_orm` method.
    """
    id: int
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True
        from_attributes = True

class UserBase(BaseModel):
    """
    Base schema for user information.

    This schema defines the basic user information, which can be used as a base for other user-related schemas.

    Attributes:
        email (EmailStr): The user's email address.
    """
    email: EmailStr

class TokenID(BaseModel):
    """
    Schema for an authentication token.

    This schema defines the structure of an authentication token, which includes the access token and the token type.

    Attributes:
        access_token (str): The access token.
        token_type (str): The type of the token (e.g., "bearer").
    """
    id: str
    user_id: int
    access_token: str
    expires_at: datetime

class UserResponse(BaseModel):
    """
    Schema for the user response.

    This schema defines the structure of the user response, which includes the user's ID, the user information, the access token, and the token type.

    Attributes:
        id (int): The user's unique identifier.
        user (UserInDB): The user information.
        access_token (str): The access token.
        token_type (str): The type of the token (e.g., "bearer").
    """
    id: int
    user: UserInDB
    access_token: str
    token_type: str