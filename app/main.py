# import os

from fastapi import FastAPI, Depends, HTTPException, exceptions
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import uvicorn
# from dotenv import load_dotenv

import models, schemas, crud
from database import SessionLocal, engine
# from app import crud

# TODO Внимание, необходимо пофиксить следующие пункты:
# TODO почистить импорты
# ...

# Создание базы данных.
# Base.metadata.create_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Зависимость для получения сессии базы данных.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Эндпоинт для получения списка всех пород.
@app.get("/breeds/")
async def get_breeds(db: Session = Depends(get_db)):
    breeds = crud.get_breeds(db)
    return breeds


# Эндпоинт для получения списка всех котят.
@app.get("/kittens/")
async def get_kittens(db: Session = Depends(get_db)):
    kittens = crud.get_kittens(db)
    return kittens


# Эндпоинт для получения одного котенка.
@app.get("/kitten/{kitten_id}")
async def get_one_kitten(kitten_id: int, db: Session = Depends(get_db)):
    kitten = crud.get_one_kitten(kitten_id, db)
    if not kitten:
        raise HTTPException(status_code=404, detail="Котенок с таким id не найден.")
    return kitten

# Эндпоинт для получения списка котят определенной породы.
@app.get("/kittens_by_breed/{breed_id}")
async def get_kittens_by_breed(breed_id: int, db: Session = Depends(get_db)):
    kittens = crud.get_kittens_by_breed(breed_id, db)
    if not kittens:
        raise HTTPException(status_code=404, detail="Котята не найдены для данной породы.")
    return kittens

# Эндпоинт для изменения информации о котенке.
@app.put("/kitten/{kitten_id}", response_model=schemas.Kitten)
async def update_kitten(kitten_id: int, kitten: schemas.KittenCreate, db: Session = Depends(get_db)):
    # kitten = db.query(Kitten).filter(Kitten.id == kitten_id).first()
    try:
        db_kitten = crud.update_kitten(kitten_id=kitten_id, kitten=kitten, db=db)
        if db_kitten is None:
            raise HTTPException(status_code=404, detail="Kitten not found")
        return db_kitten
    except exceptions.ResponseValidationError:
            print("Новые данные поданы ошибочно.")

    return {"detail": "Произошла ошибка."}


# Эндпоинт для создания информации о котенке.
@app.post("/kittens/")
async def create_kitten(kitten: schemas.KittenCreate, db: Session = Depends(get_db)):
    kitten = models.Kitten(**kitten.model_dump())
    db.add(kitten)
    db.commit()
    db.refresh(kitten)
    return kitten

# Эндпоинт для удаления информации о котенке.
@app.delete("/kittens/{kitten_id}")
async def delete_kitten(kitten_id: int, db: Session = Depends(get_db)):
    crud.delete_kitten(kitten_id, db)

    return {"detail": "Котенок успешно удален."}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
