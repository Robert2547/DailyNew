from sqlalchemy.orm import Session
from app.models.user import User
from passlib.context import CryptContext
from app.schemas.user import UserCreate

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, email: str):
    """
    Retrieve a user from the database by email.

    Args:
        db (Session): The database session.
        email (str): The email of the user to retrieve.

    Returns:
        User: The user object if found, else None.
    """
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    """
    Create a new user in the database.

    Args:
        db (Session): The database session.
        user (UserCreate): The user data to create.

    Returns:
        User: The created user object.
    """
    hashed_password = pwd_context.hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    print("User created successfully")
    return db_user


def authenticate_user(db: Session, email: str, password: str):
    """
    Authenticate a user.

    Args:
        db (Session): The database session.
        email (str): The email of the user to authenticate.
        password (str): The password to verify.

    Returns:
        User: The authenticated user object if successful, else None.
    """
    user = get_user(db, email)
    if not user or not pwd_context.verify(password, user.hashed_password):
        return None
    return user
