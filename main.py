from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, crud
from schemas import IdentifyRequest, ContactResponse

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/identify", response_model=ContactResponse)
def identify_contact(req: IdentifyRequest, db: Session = Depends(get_db)):
    return crud.identify_contact_logic(req, db)
