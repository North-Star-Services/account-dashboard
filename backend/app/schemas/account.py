from datetime import date
from typing import Optional

from pydantic import BaseModel


class AccountResponse(BaseModel):
    id: int
    name: str
    industry: str
    arr: float
    health_score: Optional[int]
    last_contact_date: Optional[date]
    owner_id: int
    owner_name: str

    class Config:
        orm_mode = True
