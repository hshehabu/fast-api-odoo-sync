from sqlalchemy.orm import Session
from fastapi import HTTPException
from api_gateway.app import models, schemas

def get_job(db: Session, job_id: int):
    return db.query(models.Job).filter(models.Job.id == job_id).first()

def get_employee(db: Session, employee_id: int):
    return db.query(models.Employee).filter(models.Employee.id == employee_id).first()

def get_employees(db: Session):
    return db.query(models.Employee).all()

def create_employee(db: Session, employee: schemas.EmployeeCreate):
    if not get_job(db, employee.job_id):
        raise HTTPException(status_code=404, detail=f"Job with id {employee.job_id} not found")
    
    db_employee = models.Employee(**employee.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def update_employee(db: Session, employee_id: int, employee: schemas.EmployeeUpdate):
    db_employee = get_employee(db, employee_id)
    if not db_employee:
        raise HTTPException(status_code=404, detail=f"Employee with id {employee_id} not found")
    
    if employee.job_id and not get_job(db, employee.job_id):
        raise HTTPException(status_code=404, detail=f"Job with id {employee.job_id} not found")
    
    for field, value in employee.model_dump().items():
        setattr(db_employee, field, value)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def delete_employee(db: Session, employee_id: int):
    employee = get_employee(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail=f"Employee with id {employee_id} not found")
    db.delete(employee)
    db.commit()
    return employee

def create_job(db: Session, job: schemas.JobCreate):
    db_job = models.Job(**job.model_dump())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def get_jobs(db: Session):
    return db.query(models.Job).all()
