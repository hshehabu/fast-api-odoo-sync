from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api_gateway.app import crud, schemas
from api_gateway.app.database import SessionLocal

router = APIRouter()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.JobBase)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    return crud.create_job(db, job)

@router.get("/", response_model=list[schemas.JobBase])
def get_job(db:Session = Depends(get_db)):
    return crud.get_jobs(db)


