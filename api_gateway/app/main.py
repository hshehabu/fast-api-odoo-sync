from fastapi import FastAPI
from api_gateway.app.routers import  employees, jobs
from api_gateway.app.database import Base, engine

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(employees.router, prefix="/employee", tags=["Employees"])
app.include_router(jobs.router, prefix="/job", tags=["Jobs"])