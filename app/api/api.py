from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserResponse
from typing import Optional
from app.services.auth import get_current_user


router = APIRouter()


@router.get("/", response_model=UserResponse)
def home(
    current_user: Optional[UserResponse] = Depends(get_current_user),
):
    """
    Retrieve the current user's information.

    Args:
        current_user (Optional[UserResponse]): The current user.

    Returns:
        UserResponse: The user's information.
    """
    if current_user:
        return current_user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )