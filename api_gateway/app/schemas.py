from pydantic import BaseModel, ConfigDict
from typing import Optional

from api_gateway.app.database import Base


class JobBase(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)

class JobCreate(JobBase):
    pass

class JobOut(JobBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class EmployeeBase(BaseModel):
    name: str
    address: str
    phone: str
    job_id: int

    model_config = ConfigDict(from_attributes=True)

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    pass

class EmployeeOut(EmployeeBase):
    id: int
    job: Optional[JobOut] = None

    model_config = ConfigDict(from_attributes=True)