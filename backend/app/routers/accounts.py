from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.repositories.account_repo import AccountRepository
from app.schemas.account import AccountResponse

router = APIRouter()


@router.get("/accounts", response_model=list[AccountResponse])
async def get_accounts(db: AsyncSession = Depends(get_db)):
    repo = AccountRepository(db)
    return await repo.get_all()
