from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin, UserInDB
from app.services.auth import create_user, authenticate_user
from app.db.base import get_db

router = APIRouter()

@router.post("/signup", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user account.

    Args:
        user (UserCreate): The user data for account creation.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If a user with the given email already exists.

    Returns:
        UserInDB: The created user object.
    """
    db_user = create_user(db, user)
    print("Signup user", db_user)
    if not db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return db_user

@router.post("/login", response_model=UserInDB)
def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate a user and log them in.

    Args:
        user (UserLogin): The user login credentials.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the login credentials are invalid.

    Returns:
        UserInDB: The authenticated user object.
    """
    db_user = authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return db_user