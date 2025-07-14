from pydantic import BaseModel

class SongCreate(BaseModel):
    title: str
    artist: str

class SongOut(SongCreate):
    id: int

    class Config:
        orm_mode = True
