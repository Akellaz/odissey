import sys
# для настройки баз данных
from sqlalchemy import Column, ForeignKey, Integer, String

# для определения таблицы и модели
from sqlalchemy.ext.declarative import declarative_base

# для создания отношений между таблицами
from sqlalchemy.orm import relationship

# для настроек
from sqlalchemy import create_engine

# создание экземпляра declarative_base
Base = declarative_base()


# мы создаем класс Book наследуя его из класса Base.
class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    date = Column(String(250), nullable=False)
    time = Column(String(250))
    author = Column(String(250), nullable=False)


# создает экземпляр create_engine в конце файла
engine = create_engine('sqlite:///ak_data.db')

Base.metadata.create_all(engine)
