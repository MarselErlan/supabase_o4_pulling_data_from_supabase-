from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models import Film as FilmModel  # Use alias to avoid conflict
from schemas import FilmCreate, Film as FilmSchema  # Use alias for clarity
from typing import List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Film Management API")

# Dependencies
def get_db_session():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()

@app.post("/films/", response_model=FilmSchema, status_code=201)
async def create_film(film: FilmCreate, db: Session = Depends(get_db_session)):
    db_film = FilmModel(**film.dict())
    db.add(db_film)
    db.commit()
    db.refresh(db_film)
    logger.info(f"Created film with ID {db_film.id}")
    return db_film

@app.get("/films/", response_model=List[FilmSchema])
async def read_films(db: Session = Depends(get_db_session), skip: int = 0, limit: int = 100):
    films = db.query(FilmModel).offset(skip).limit(limit).all()
    logger.info(f"Retrieved {len(films)} films")
    return films

@app.get("/films/{film_id}", response_model=FilmSchema)
async def read_film(film_id: int, db: Session = Depends(get_db_session)):
    film = db.query(FilmModel).filter(FilmModel.id == film_id).first()
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    return film

@app.put("/films/{film_id}", response_model=FilmSchema)
async def update_film(film_id: int, film: FilmCreate, db: Session = Depends(get_db_session)):
    db_film = db.query(FilmModel).filter(FilmModel.id == film_id).first()
    if not db_film:
        raise HTTPException(status_code=404, detail="Film not found")
    update_data = film.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_film, key, value)
    db.commit()
    db.refresh(db_film)
    return db_film

@app.delete("/films/{film_id}", status_code=204)
async def delete_film(film_id: int, db: Session = Depends(get_db_session)):
    db_film = db.query(FilmModel).filter(FilmModel.id == film_id).first()
    if not db_film:
        raise HTTPException(status_code=404, detail="Film not found")
    db.delete(db_film)
    db.commit()