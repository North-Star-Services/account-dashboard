from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.account import Account


class AccountRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[Account]:
        result = await self.db.execute(select(Account))
        return list(result.scalars().all())

    async def get_by_id(self, account_id: int) -> Account | None:
        result = await self.db.execute(select(Account).where(Account.id == account_id))
        return result.scalar_one_or_none()
