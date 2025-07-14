from pydantic import BaseModel
from typing import List

class SongCreate(BaseModel):
    title: str
    embedding: List[float]
    cluster: int

class SongOut(SongCreate):
    id: int

    class Config:
        orm_mode = True
