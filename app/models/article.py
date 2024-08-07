from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Article(Base):
    """
    Article model representing the 'articles' table in the database.

    Attributes:
        id (int): The primary key of the article.
        title (str): The title of the article.
        content (str): The full content of the article.
        summary (str): The summarized content of the article.
        url (str): The URL source of the article.
        created_at (datetime): The timestamp when the article was created.
        author_id (int): The foreign key referencing the author (User) of the article.
        author (relationship): Relationship to the User model.

    Note:
        The 'created_at' field is automatically set to the current timestamp when a new article is created.
    """

    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    summary = Column(Text)
    url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="articles")
