from sqlalchemy import Column, Integer, String, DateTime
from db import Base

class Film(Base):
    __tablename__ = "film"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    created_at = Column(DateTime)