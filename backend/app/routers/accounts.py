from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.account_repo import AccountRepository
from app.schemas.account import AccountResponse

router = APIRouter()


@router.get("/accounts", response_model=List[AccountResponse])
def get_accounts(db: Session = Depends(get_db)):
    repo = AccountRepository(db)
    return repo.get_all()
