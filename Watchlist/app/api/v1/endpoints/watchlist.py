from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import base as deps
from app.core.auth import get_current_user
from app.schemas.watchlist import (
    WatchlistItemCreate,
    WatchlistItemResponse,
    WatchlistResponse,
)
from app.services.watchlist_services import WatchlistService
from typing import List
import logging

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/", response_model=WatchlistResponse)
async def get_watchlist(
    db: Session = Depends(deps.get_db), current_user: dict = Depends(get_current_user)
):
    try:
        items = await WatchlistService.get_user_watchlist(db, current_user["id"])
        return WatchlistResponse(items=items, total=len(items))
    except Exception as e:
        logger.error(f"Watchlist error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Error fetching watchlist: {str(e)}"
        )


@router.post(
    "/",
    response_model=WatchlistItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add stock to watchlist",
)
async def add_to_watchlist(
    stock_data: WatchlistItemCreate,
    db: Session = Depends(deps.get_db),
    current_user: dict = Depends(get_current_user),
):
    return await WatchlistService.add_stock(db, current_user["id"], stock_data)


@router.delete(
    "/{symbol}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove stock from watchlist",
)
async def remove_from_watchlist(
    symbol: str,
    db: Session = Depends(deps.get_db),
    current_user: dict = Depends(get_current_user),
):
    await WatchlistService.remove_stock(db, current_user["id"], symbol)


@router.get(
    "/check/{symbol}", response_model=bool, summary="Check if stock is in watchlist"
)
async def check_watchlist_status(
    symbol: str,
    db: Session = Depends(deps.get_db),
    current_user: dict = Depends(get_current_user),
):
    return await WatchlistService.check_stock_in_watchlist(
        db, current_user["id"], symbol
    )
