from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import schemas, database, models, JWT_token
from hashing import Hash


router = APIRouter(tags=["Authentication"])

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User does not exist")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=404, detail=f"Invalid credentials")
    
    access_token = JWT_token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}