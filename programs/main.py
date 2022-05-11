from fastapi import FastAPI
import models
from database import engine
from routers import program

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(program.router)





# @app.post("/user", status_code=201, response_model=schemas.ShowUser, tags=["users"])
# def create_user(request: schemas.User, db: Session = Depends(get_db)):
#     new_user = models.User(name=request.name, email=request.email, password=hashing.Hash.bcrypt(request.password))
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user


# @app.get("/user/{id}", status_code=200, response_model=schemas.ShowUserPrograms, tags=["users"])
# def get_user(id: int, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail=f"User with the id {id} is not found")
#     return user
