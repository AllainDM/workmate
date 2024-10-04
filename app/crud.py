
import sqlalchemy
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import models, schemas
from database import get_db


# Получение списка всех пород.
def get_breeds(db: Session = Depends(get_db)):
    breeds = db.query(models.Breed).all()
    return breeds


# Получение списка всех котят.
def get_kittens(db: Session = Depends(get_db)):
    kittens = db.query(models.Kitten).all()
    return kittens


# Получение одного котенка.
def get_one_kitten(kitten_id: int, db: Session = Depends(get_db)):
    kitten = db.query(models.Kitten).filter(models.Kitten.id == kitten_id).first()  #models.Kitten.id == kitten_id).first()
    if not kitten:
        raise HTTPException(status_code=404, detail="Котенок с таким id не найден.")
    return kitten

# Получение списка котят определенной породы.
def get_kittens_by_breed(breed_id: int, db: Session = Depends(get_db)):
    kittens = db.query(models.Kitten).filter(models.Kitten.breed_id == breed_id).all()
    if not kittens:
        raise HTTPException(status_code=404, detail="Котята не найдены для данной породы.")
    return kittens

# Изменение информации о котенке.
def update_kitten(kitten_id: int, kitten: schemas.KittenCreate, db: Session = Depends(get_db)):
    db_kitten = get_one_kitten(kitten_id, db)
    print(f"db_kitten {db_kitten}")
    if db_kitten:
        try:
            for key, value in kitten.model_dump().items():
                if value == 0 or value == "string":
                    continue
                setattr(db_kitten, key, value)
            db.commit()
            db.refresh(db_kitten)
        except sqlalchemy.exc.IntegrityError:
            print("Новые данные поданы ошибочно 1.")
        # except exceptions.ResponseValidationError:
        #     print("Новые данные поданы ошибочно 2.")

    return db_kitten


# Создание информации о котенке.
def create_kitten(name: str, color: str, age_months: int, description: str, breed_id: int, db: Session = Depends(get_db)):
    kitten = models.Kitten(name=name, color=color, age_months=age_months, description=description, breed_id=breed_id)
    db.add(kitten)
    db.commit()
    db.refresh(kitten)
    return kitten

# Удаление информации о котенке.
def delete_kitten(kitten_id: int, db: Session = Depends(get_db)):
    kitten = db.query(models.Kitten).filter(models.Kitten.id == kitten_id).first()
    if not kitten:
        raise HTTPException(status_code=404, detail="Котенок не найден.")

    db.delete(kitten)
    db.commit()
    return {"detail": "Котенок успешно удален."}
