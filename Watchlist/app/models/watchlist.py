from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint, Index
from sqlalchemy.sql import func
from app.db.base import Base


class WatchlistItem(Base):
    __tablename__ = "watchlist_items"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, index=True, nullable=False
    )  # References AuthService user ID
    symbol = Column(String, nullable=False)
    name = Column(String)  # Company name
    sector = Column(String)
    added_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "symbol", name="uix_user_symbol"),
        Index("idx_user_symbol", user_id, symbol),
    )
