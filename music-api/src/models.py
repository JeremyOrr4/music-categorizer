from sqlalchemy import Column, Integer, String, JSON
from src.database import Base

class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    embedding = Column(JSON)
    cluster = Column(Integer)
