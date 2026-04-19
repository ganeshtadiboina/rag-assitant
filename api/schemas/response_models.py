from pydantic import BaseModel
from typing import List, Dict


class QueryResponse(BaseModel):
    answer: str
    sources: List[Dict]