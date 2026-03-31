import asyncio
import random
from datetime import date, timedelta

from app.database import Base, async_session, engine
from app.models.account import Account

INDUSTRIES = [
    "Technology",
    "Healthcare",
    "Financial Services",
    "Manufacturing",
    "Retail",
    "Education",
    "Media & Entertainment",
    "Energy",
    "Transportation",
    "Professional Services",
]

OWNERS = [
    (1, "Sarah Chen"),
    (2, "Marcus Johnson"),
    (3, "Emily Rodriguez"),
    (4, "David Kim"),
    (5, "Rachel Thompson"),
    (6, "James Wilson"),
    (7, "Priya Patel"),
    (8, "Michael Brown"),
    (9, "Lisa Garcia"),
    (10, "Tom Anderson"),
]

COMPANY_PREFIXES = [
    "Apex", "Nova", "Vertex", "Summit", "Catalyst", "Pinnacle", "Vanguard",
    "Horizon", "Meridian", "Atlas", "Zenith", "Forge", "Pulse", "Nexus",
    "Crest", "Prime", "Core", "Edge", "Arc", "Flux", "Orbit", "Sigma",
    "Delta", "Omni", "Quantum", "Radiant", "Sterling", "Titan", "Vector",
    "Wave", "Astra", "Bolt", "Cipher", "Drift", "Echo", "Fuse", "Grid",
    "Helix", "Ion", "Jade", "Kinetic", "Lumen", "Matrix", "Nebula", "Opal",
]

COMPANY_SUFFIXES = [
    "Systems", "Solutions", "Technologies", "Group", "Corp", "Industries",
    "Labs", "Analytics", "Dynamics", "Ventures", "Networks", "Digital",
    "Global", "Partners", "Innovations", "Consulting", "Services", "Inc",
    "Platforms", "Software", "Data", "Cloud", "Logic", "Works", "Hub",
]


def generate_company_name(index: int) -> str:
    prefix = random.choice(COMPANY_PREFIXES)
    suffix = random.choice(COMPANY_SUFFIXES)
    if index > len(COMPANY_PREFIXES) * len(COMPANY_SUFFIXES):
        return f"{prefix} {suffix} {index}"
    return f"{prefix} {suffix}"


async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as db:
        # Clear existing data
        from sqlalchemy import delete

        await db.execute(delete(Account))
        await db.commit()

        random.seed(42)

        today = date.today()

        accounts = []
        used_names: set[str] = set()

        null_contact_indices = set(random.sample(range(5000), 400))
        zero_health_indices = set(random.sample(range(5000), 250))
        null_health_indices = set(random.sample(range(5000), 100))
        zero_health_indices -= null_health_indices

        for i in range(5000):
            name = generate_company_name(i)
            while name in used_names:
                name = f"{random.choice(COMPANY_PREFIXES)} {random.choice(COMPANY_SUFFIXES)} {i}"
            used_names.add(name)

            industry = random.choice(INDUSTRIES)
            arr = round(random.uniform(10000, 5000000), 2)
            owner_id, owner_name = random.choice(OWNERS)

            if i in null_health_indices:
                health_score = None
            elif i in zero_health_indices:
                health_score = 0
            else:
                health_score = random.randint(1, 100)

            if i in null_contact_indices:
                last_contact_date = None
            else:
                days_ago = random.randint(0, 730)
                last_contact_date = today - timedelta(days=days_ago)

            account = Account(
                name=name,
                industry=industry,
                arr=arr,
                health_score=health_score,
                last_contact_date=last_contact_date,
                owner_id=owner_id,
                owner_name=owner_name,
            )
            accounts.append(account)

        db.add_all(accounts)
        await db.commit()

    print(f"Seeded {len(accounts)} accounts.")

    async with async_session() as db:
        from sqlalchemy import func, select

        total = (await db.execute(select(func.count(Account.id)))).scalar()
        null_contacts = (
            await db.execute(
                select(func.count(Account.id)).where(Account.last_contact_date.is_(None))
            )
        ).scalar()
        zero_health = (
            await db.execute(
                select(func.count(Account.id)).where(Account.health_score == 0)
            )
        ).scalar()
        null_health = (
            await db.execute(
                select(func.count(Account.id)).where(Account.health_score.is_(None))
            )
        ).scalar()

    print(f"  Total: {total}")
    print(f"  Null last_contact_date: {null_contacts}")
    print(f"  Health score = 0: {zero_health}")
    print(f"  Health score = null: {null_health}")


if __name__ == "__main__":
    asyncio.run(seed())
