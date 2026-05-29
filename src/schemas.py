from pydantic import BaseModel, Field
from typing import List, Optional

# ── 工资明细 ──
class WageDetailBase(BaseModel):
    name: str
    type: str
    amount: int

    model_config = {"from_attributes": True}

class WageDetailCreate(WageDetailBase):
    pass

class WageDetail(WageDetailBase):
    id: int
    employee_id: int

    model_config = {"from_attributes": True}

# ── 登录 ──
class LoginRequest(BaseModel):
    name: str
    password: str

class LoginResponse(BaseModel):
    id: int
    name: str
    role: str

    model_config = {"from_attributes": True}

# ── 员工（响应不含密码）──
class EmployeeBase(BaseModel):
    name: str
    role: Optional[str] = "employee"
    gender: Optional[str] = None
    birthday: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    education: Optional[str] = None
    school: Optional[str] = None
    major: Optional[str] = None
    marital_status: Optional[str] = Field(None, alias="maritalStatus")
    job_title: Optional[str] = Field(None, alias="jobTitle")
    status: Optional[str] = "active"
    wage_details: List[WageDetail] = Field(default=[], alias="wageDetails")

    model_config = {"from_attributes": True, "populate_by_name": True}

class EmployeeCreate(EmployeeBase):
    password: Optional[str] = "123456"

class EmployeeUpdate(EmployeeBase):
    password: Optional[str] = None
    wage_details: Optional[List[WageDetailCreate]] = Field(None, alias="wageDetails")
    model_config = {"from_attributes": True, "populate_by_name": True}

class Employee(EmployeeBase):
    id: int
    wage_details: List[WageDetail] = Field(default=[], alias="wageDetails")

    model_config = {"from_attributes": True, "populate_by_name": True}

class StatusUpdate(BaseModel):
    status: str