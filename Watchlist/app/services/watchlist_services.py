from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.models.watchlist import WatchlistItem
from app.schemas.watchlist import WatchlistItemCreate
from typing import List
import logging

logger = logging.getLogger(__name__)


class WatchlistService:
    @staticmethod
    async def get_user_watchlist(db: Session, user_id: int) -> List[WatchlistItem]:
        return db.query(WatchlistItem).filter(WatchlistItem.user_id == user_id).all()

    @staticmethod
    async def add_stock(
        db: Session, user_id: int, stock_data: WatchlistItemCreate
    ) -> WatchlistItem:
        try:
            watchlist_item = WatchlistItem(user_id=user_id, **stock_data.model_dump())
            db.add(watchlist_item)
            db.commit()
            db.refresh(watchlist_item)
            return watchlist_item
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Stock already in watchlist",
            )

    @staticmethod
    async def remove_stock(db: Session, user_id: int, symbol: str) -> None:
        result = (
            db.query(WatchlistItem)
            .filter(WatchlistItem.user_id == user_id, WatchlistItem.symbol == symbol)
            .delete()
        )

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Stock not found in watchlist",
            )

        db.commit()

    @staticmethod
    async def check_stock_in_watchlist(db: Session, user_id: int, symbol: str) -> bool:
        return (
            db.query(WatchlistItem)
            .filter(WatchlistItem.user_id == user_id, WatchlistItem.symbol == symbol)
            .first()
            is not None
        )
