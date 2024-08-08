from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin, UserInDB
from app.services.auth import create_user, authenticate_user
from app.db.base import get_db
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta
from app.services.auth import create_access_token, create_password_reset_token, reset_password

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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
def login(form_data: OAuth2PasswordBearer = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate a user and log them in.

    Args:
        user (UserLogin): The user login credentials.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the login credentials are invalid.

    Returns:
        returns a dictionary with the access token and token type.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/password-reset-request")
async def request_password_reset(email: str, db: Session = Depends(get_db)):
    token = create_password_reset_token(db, email)
    # Here you would typically send an email with the reset token
    return {"message": "If the email exists in our system, a password reset link has been sent."}

@router.post("/password-reset")
async def perform_password_reset(token: str, new_password: str, db: Session = Depends(get_db)):
    if reset_password(db, token, new_password):
        return {"message": "Password reset successfully"}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password reset failed")