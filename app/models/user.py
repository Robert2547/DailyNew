from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base

class User(Base):
    """
    User model representing the 'users' table in the database.

    Attributes:
        id (int): The primary key of the user.
        email (str): The user's email address (unique).
        hashed_password (str): The hashed password of the user.
        is_active (bool): Whether the user account is active.
        is_superuser (bool): Whether the user has superuser privileges.
        articles (relationship): Relationship to the user's articles.

    Note:
        The 'articles' relationship is defined with lazy="dynamic" to allow for efficient querying.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    articles = relationship("Article", back_populates="author", lazy="dynamic")


class TokenInfo(Base):
    __tablename__ = "token_info"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    access_token = Column(String)
    expires_at = Column(DateTime)