from datetime import date

from pydantic import BaseModel, ConfigDict


class AccountResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    industry: str
    arr: float
    health_score: int | None
    last_contact_date: date | None
    owner_id: int
    owner_name: str
