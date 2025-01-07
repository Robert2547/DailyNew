from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class WatchlistItemBase(BaseModel):
    symbol: str
    name: Optional[str] = None
    sector: Optional[str] = None


class WatchlistItemCreate(WatchlistItemBase):
    pass


class WatchlistItemResponse(WatchlistItemBase):
    id: int
    user_id: int
    added_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class WatchlistResponse(BaseModel):
    items: List[WatchlistItemResponse]
    total: int
