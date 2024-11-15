"""Article model for storing summarized news."""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    summary = Column(Text)
    url = Column(String)
    published_date = Column(DateTime, default=datetime.utcnow)
    author_id = Column(Integer, ForeignKey("users.id"))
    
    author = relationship("User", back_populates="articles")