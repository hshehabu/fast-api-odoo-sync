from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from api_gateway.app.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    employees = relationship("Employee", back_populates="job")

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    phone = Column(String)
    job_id = Column(Integer, ForeignKey("jobs.id"))

    job = relationship("Job", back_populates="employees")