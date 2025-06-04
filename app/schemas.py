from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FilmBase(BaseModel):
    title: str
    description: Optional[str] = None

class FilmCreate(FilmBase):
    pass

class Film(FilmBase):
    id: int
    created_at: datetime  # Changed from str to datetime

    class Config:
        from_attributes = True