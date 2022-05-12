from fastapi import HTTPException
from sqlalchemy.orm import Session
import models, schemas



def get_all(db: Session):
    programs = db.query(models.Program).all()
    return programs

def create(request:schemas.Program, db: Session):
    new_program = models.Program(title=request.title, body=request.body, user_id=1)
    db.add(new_program)
    db.commit()
    db.refresh(new_program)
    return new_program

def get_one(id: int, db: Session):
    program = db.query(models.Program).filter(models.Program.id == id).first()
    if not program:
        raise HTTPException(status_code=404, detail=f"Program with the id {id} is not found")
    return program

def update(id: int, request: schemas.Program, db: Session):
    program = db.query(models.Program).filter(models.Program.id == id)
    if not program.first():
        raise HTTPException(status_code=404, detail=f"Program with the id {id} is not found")
    program.update(request.dict())
    db.commit()
    return f"Updated program with id {id}"

def delete(id: int, db: Session):
    program = db.query(models.Program).filter(models.Program.id == id)
    if not program.first():
        raise HTTPException(status_code=404, detail=f"Program with the id {id} is not found")
    program.delete(synchronize_session=False)
    db.commit()
    return f"Deleted program with id {id}"