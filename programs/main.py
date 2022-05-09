from fastapi import FastAPI, Depends
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
def program(limit=10, published: bool = True, sort: Optional[str] = None):
    if published:
        return {"data": f"{limit} published blogs from the list"}
    else:
        return {"data": f"{limit} blogs from the list"}


@app.post("/program")
def create(request: schemas.Program, db: Session = Depends(get_db)):
    new_program = models.Program(title=request.title, body=request.body)
    db.add(new_program)
    db.commit()
    db.refresh(new_program)
    return new_program


@app.get("/program/{id}")
def get_program(id: int):
    return {"data": id}
