from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Wallet(Base):
    __tablename__ = 'wallet'

    id = Column(Integer, primary_key=True)
    description = Column(String(50), nullable=False)
    password = Column(String(32), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=True)
