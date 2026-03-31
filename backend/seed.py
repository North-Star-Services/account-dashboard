import random
from datetime import date, timedelta

from app.database import Base, SessionLocal, engine
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
    # Add a number occasionally to ensure uniqueness across 5000 records
    if index > len(COMPANY_PREFIXES) * len(COMPANY_SUFFIXES):
        return f"{prefix} {suffix} {index}"
    return f"{prefix} {suffix}"


def seed():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    # Clear existing data
    db.query(Account).delete()
    db.commit()

    random.seed(42)  # Reproducible data

    today = date.today()
    two_years_ago = today - timedelta(days=730)

    accounts = []
    used_names = set()

    # Distribution plan for 5000 records:
    # - 400 with null last_contact_date
    # - 250 with health_score = 0
    # - 100 with health_score = null
    # - remaining 4250 with normal distributed data

    null_contact_indices = set(random.sample(range(5000), 400))
    zero_health_indices = set(random.sample(range(5000), 250))
    null_health_indices = set(random.sample(range(5000) , 100))

    # Remove overlaps: null_health takes priority over zero_health
    zero_health_indices -= null_health_indices

    for i in range(5000):
        # Generate unique company name
        name = generate_company_name(i)
        while name in used_names:
            name = f"{random.choice(COMPANY_PREFIXES)} {random.choice(COMPANY_SUFFIXES)} {i}"
        used_names.add(name)

        industry = random.choice(INDUSTRIES)
        arr = round(random.uniform(10000, 5000000), 2)
        owner_id, owner_name = random.choice(OWNERS)

        # Health score logic
        if i in null_health_indices:
            health_score = None
        elif i in zero_health_indices:
            health_score = 0
        else:
            health_score = random.randint(1, 100)

        # Last contact date logic
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

    db.bulk_save_objects(accounts)
    db.commit()
    db.close()

    print(f"Seeded {len(accounts)} accounts.")

    # Print distribution summary
    db = SessionLocal()
    total = db.query(Account).count()
    null_contacts = db.query(Account).filter(Account.last_contact_date.is_(None)).count()
    zero_health = db.query(Account).filter(Account.health_score == 0).count()
    null_health = db.query(Account).filter(Account.health_score.is_(None)).count()
    db.close()

    print(f"  Total: {total}")
    print(f"  Null last_contact_date: {null_contacts}")
    print(f"  Health score = 0: {zero_health}")
    print(f"  Health score = null: {null_health}")


if __name__ == "__main__":
    seed()
