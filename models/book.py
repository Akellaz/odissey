from sqlalchemy import Column, Integer, String, Date, Time
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    author = Column(String(250))
    date = Column(Date)
    time = Column(Time)
    
    def __init__(self, name, date, time, author=None):
        self.name = name
        self.author = author
        self.date = date
        self.time = time
