from fastapi import FastAPI, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
import schemas, models, hashing
from database import engine, SessionLocal


app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/program", response_model=List[schemas.ShowProgram], tags=["programs"])
def all(db: Session = Depends(get_db)):
    programs = db.query(models.Program).all()
    return programs


@app.post("/program", status_code=201, response_model=schemas.Program, tags=["programs"])
def create(request: schemas.Program, db: Session = Depends(get_db)):
    new_program = models.Program(title=request.title, body=request.body, user_id=1)
    db.add(new_program)
    db.commit()
    db.refresh(new_program)
    return new_program


@app.get("/program/{id}", status_code=200, response_model=schemas.ShowProgram, tags=["programs"])
def show(id: int, response: Response, db: Session = Depends(get_db)):
    program = db.query(models.Program).filter(models.Program.id == id).first()
    if not program:
        raise HTTPException(status_code=404, detail=f"Program with the id {id} is not found")
    return program


@app.put("/program/{id}", status_code=202, tags=["programs"])
def update(id: int, request: schemas.Program, db: Session = Depends(get_db)):
    program = db.query(models.Program).filter(models.Program.id == id)
    if not program.first():
        raise HTTPException(status_code=404, detail=f"Program with the id {id} is not found")
    program.update(request.dict())
    db.commit()
    return f"Updated program with id {id}"


@app.delete("/program/{id}", status_code=200, tags=["programs"])
def delete(id: int, db: Session = Depends(get_db)):
    program = db.query(models.Program).filter(models.Program.id == id)
    if not program.first():
        raise HTTPException(status_code=404, detail=f"Program with the id {id} is not found")
    program.delete(synchronize_session=False)
    db.commit()
    return f"Deleted program with id {id}"


@app.post("/user", status_code=201, response_model=schemas.ShowUser, tags=["users"])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/user/{id}", status_code=200, response_model=schemas.ShowUserPrograms, tags=["users"])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with the id {id} is not found")
    return user
