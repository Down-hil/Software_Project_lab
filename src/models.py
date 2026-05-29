from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum

class EmployeeStatus(str, enum.Enum):
    active = "active"
    resigned = "resigned"
    transfer = "transfer"
    retired = "retired"

class EmployeeRole(str, enum.Enum):
    admin = "admin"
    employee = "employee"

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    password = Column(String, default="123456")  # 默认密码
    role = Column(String, default=EmployeeRole.employee)  # admin / employee
    gender = Column(String)
    birthday = Column(String)  # 前端传 "YYYY-MM-DD"
    phone = Column(String)
    email = Column(String)
    education = Column(String)
    school = Column(String)
    major = Column(String)
    marital_status = Column(String)
    job_title = Column(String)
    status = Column(String, default=EmployeeStatus.active)

    wage_details = relationship("WageDetail", back_populates="employee", cascade="all, delete-orphan")

class WageType(str, enum.Enum):
    income = "income"
    deduction = "deduction"

class WageDetail(Base):
    __tablename__ = "wage_details"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(String)  # income / deduction
    amount = Column(Integer, default=0)
    employee_id = Column(Integer, ForeignKey("employees.id"))

    employee = relationship("Employee", back_populates="wage_details")