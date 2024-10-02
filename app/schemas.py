from pydantic import BaseModel
from typing import Optional, List

class BreedBase(BaseModel):
    name: str

class BreedCreate(BreedBase):
    pass

class Breed(BreedBase):
    id: int
    class Config:
        orm_mode = True

class KittenBase(BaseModel):
    name: str
    color: str
    age_months: int
    description: Optional[str] = None
    breed_id: int

class KittenCreate(KittenBase):
    pass

class Kitten(KittenBase):
    id: int
    breed: Breed
    class Config:
        orm_mode = True