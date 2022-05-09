from sqlalchemy import Column, Integer, String
from database import Base

class Program(Base):
    __tablename__ = 'programs'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)