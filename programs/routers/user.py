from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas, database, models
from hashing import Hash

from repository import user

router = APIRouter(prefix="/user", tags=["Users"])
get_db = database.get_db


@router.get("/{id}", status_code=200, response_model=schemas.ShowUserPrograms)
def get_user(id: int, db: Session = Depends(get_db)):
    return user.get_user(id, db)


@router.post("/", status_code=201, response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(db)