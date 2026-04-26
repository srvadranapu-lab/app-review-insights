from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class RawReview(BaseModel):
    id: str
    product: str
    source: str  # appstore | playstore
    rating: int
    title: str
    body: str
    date: datetime

class PulseSummary(BaseModel):
    product: str
    window: str  # date range as string
    top_themes: List[str]
    quotes: List[str]
    action_ideas: List[str]
