from fastapi import FastAPI, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
import schemas, models
from database import engine, SessionLocal


app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def index():
    return {"data": {"name": "Dexter"}}


@app.get("/program")
def all(db: Session = Depends(get_db)):
    programs = db.query(models.Program).all()
    return programs


@app.post("/program", status_code=201)
def create(request: schemas.Program, db: Session = Depends(get_db)):
    new_program = models.Program(title=request.title, body=request.body)
    db.add(new_program)
    db.commit()
    db.refresh(new_program)
    return new_program


@app.delete("/program/{id}", status_code=200)
def delete(id: int, db: Session = Depends(get_db)):
    program = db.query(models.Program).filter(models.Program.id == id).first()
    if not program:
        raise HTTPException(status_code=404, detail=f"Program with the id {id} is not available")
    db.query(models.Program).filter(models.Program.id == id).delete(synchronize_session=False)
    db.commit()
    return f'Deleted program with id {id}'
    

@app.get("/program/{id}")
def single(id: int, response: Response, db: Session = Depends(get_db)):
    program = db.query(models.Program).filter(models.Program.id == id).first()
    if not program:
        raise HTTPException(status_code=404, detail=f"Program with the id {id} is not available")
    return program
