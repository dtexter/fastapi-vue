from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException, Response

import schemas, database, models


router = APIRouter(prefix="", tags=["Blogs"])



get_db = database.get_db


@router.get("/", response_model=List[schemas.ShowProgram])
def all(db: Session = Depends(database.get_db)):
    programs = db.query(models.Program).all()
    return programs


@router.post("/", status_code=201, response_model=schemas.Program)
def create(request: schemas.Program, db: Session = Depends(get_db)):
    new_program = models.Program(title=request.title, body=request.body, user_id=1)
    db.add(new_program)
    db.commit()
    db.refresh(new_program)
    return new_program


@router.get("/{id}", status_code=200, response_model=schemas.ShowProgram)
def show(id: int, response: Response, db: Session = Depends(get_db)):
    program = db.query(models.Program).filter(models.Program.id == id).first()
    if not program:
        raise HTTPException(status_code=404, detail=f"Program with the id {id} is not found")
    return program


@router.put("/{id}", status_code=202)
def update(id: int, request: schemas.Program, db: Session = Depends(get_db)):
    program = db.query(models.Program).filter(models.Program.id == id)
    if not program.first():
        raise HTTPException(status_code=404, detail=f"Program with the id {id} is not found")
    program.update(request.dict())
    db.commit()
    return f"Updated program with id {id}"


@router.delete("/{id}", status_code=200)
def delete(id: int, db: Session = Depends(get_db)):
    program = db.query(models.Program).filter(models.Program.id == id)
    if not program.first():
        raise HTTPException(status_code=404, detail=f"Program with the id {id} is not found")
    program.delete(synchronize_session=False)
    db.commit()
    return f"Deleted program with id {id}"