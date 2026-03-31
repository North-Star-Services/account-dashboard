from sqlalchemy import Column, Integer, String, Float, Date

from app.database import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    industry = Column(String, nullable=False)
    arr = Column(Float, nullable=False)
    health_score = Column(Integer, nullable=True)
    last_contact_date = Column(Date, nullable=True)
    owner_id = Column(Integer, nullable=False)
    owner_name = Column(String, nullable=False)
