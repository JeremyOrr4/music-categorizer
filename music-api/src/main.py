from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import SessionLocal, engine
from src import models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/songs/", response_model=schemas.SongOut)
def create_song(song: schemas.SongCreate, db: Session = Depends(get_db)):
    db_song = models.Song(**song.dict())
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song

@app.get("/songs/", response_model=list[schemas.SongOut])
def read_songs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Song).offset(skip).limit(limit).all()

@app.get("/songs_all/", response_model=list[schemas.SongOut])
def read_all_songs(db: Session = Depends(get_db)):
    return db.query(models.Song).all()

@app.get("/songs/{song_id}", response_model=schemas.SongOut)
def read_song(song_id: int, db: Session = Depends(get_db)):
    song = db.query(models.Song).filter(models.Song.id == song_id).first()
    if song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    return song

# @app.put("/songs/{song_id}", response_model=schemas.SongOut)
# def update_song(song_id: int, song_update: schemas.SongCreate, db: Session = Depends(get_db)):
#     song = db.query(models.Song).filter(models.Song.id == song_id).first()
#     if song is None:
#         raise HTTPException(status_code=404, detail="Song not found")

#     for key, value in song_update.dict().items():
#         setattr(song, key, value)

#     db.commit()
#     db.refresh(song)
#     return song

# @app.delete("/songs/{song_id}")
# def delete_song(song_id: int, db: Session = Depends(get_db)):
#     song = db.query(models.Song).filter(models.Song.id == song_id).first()
#     if song is None:
#         raise HTTPException(status_code=404, detail="Song not found")

#     db.delete(song)
#     db.commit()
#     return {"message": "Song deleted successfully"}
