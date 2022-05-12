from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException, Response
import schemas, database, models, oauth2

from repository import program


router = APIRouter(prefix="/program", tags=["Programs"])
get_db = database.get_db


@router.get("/", response_model=List[schemas.ShowProgram])
def all(db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return program.get_all(db)


@router.post("/", status_code=201, response_model=schemas.Program)
def create(request: schemas.Program, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return program.create(request, db)


@router.get("/{id}", status_code=200, response_model=schemas.ShowProgram)
def show(id: int, response: Response, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return program.get_one(id, db)


@router.put("/{id}", status_code=202)
def update(id: int, request: schemas.Program, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return program.update(id, request, db)


@router.delete("/{id}", status_code=200)
def delete(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return program.delete(id, db)
