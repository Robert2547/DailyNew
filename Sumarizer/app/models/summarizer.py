from dataclasses import dataclass
from typing import List

@dataclass
class SummaryRequest:
    content: str
    max_length: int | None = None
    min_length: int | None = None

@dataclass
class SummaryResponse:
    summary: str
    processing_time: float
    chunks_processed: int