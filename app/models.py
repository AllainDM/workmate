from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# from app.database import Base
# from database import Base
from database import Base


# Определение модели породы.
class Breed(Base):
    __tablename__ = 'breeds'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    kittens = relationship("Kitten", back_populates="breed")

# Определение модели котенка.
class Kitten(Base):
    __tablename__ = 'kittens'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    color = Column(String, index=True)
    age_months = Column(Integer)
    description = Column(String)
    breed_id = Column(Integer, ForeignKey('breeds.id'))

    breed = relationship("Breed", back_populates="kittens")