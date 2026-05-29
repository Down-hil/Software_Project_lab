from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# ── 启动时初始化默认管理员 ──
@app.on_event("startup")
def seed_default_admin():
    db = SessionLocal()
    try:
        existing_admin = db.query(models.Employee).filter(
            models.Employee.role == "admin"
        ).first()
        if not existing_admin:
            admin = models.Employee(
                name="admin",
                password="123456",
                role="admin",
                gender="男",
                marital_status="已婚",
                job_title="系统管理员",
                status="active",
            )
            db.add(admin)
            db.commit()
    finally:
        db.close()

# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Vue 开发服务器地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 依赖项
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ── 登录 ──
@app.post("/api/login", response_model=schemas.LoginResponse)
def login(login_data: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = crud.authenticate_employee(db, login_data.name, login_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    return user

# ── 员工自助：查看自己的工资条 ──
@app.get("/api/my-wage/{employee_id}", response_model=schemas.Employee, response_model_by_alias=True)
def get_my_wage(employee_id: int, db: Session = Depends(get_db)):
    employee = crud.get_my_wage(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="员工不存在")
    return employee

# ── 管理员：员工列表 ──
@app.get("/api/employees", response_model=list[schemas.Employee], response_model_by_alias=True)
def read_employees(
    status: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    employees = crud.get_employees(db, status=status, search=search)
    return employees

@app.post("/api/employees", response_model=schemas.Employee, response_model_by_alias=True)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return crud.create_employee(db, employee)

@app.put("/api/employees/{employee_id}", response_model=schemas.Employee, response_model_by_alias=True)
def update_employee(employee_id: int, employee: schemas.EmployeeUpdate, db: Session = Depends(get_db)):
    db_employee = crud.update_employee(db, employee_id, employee)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

@app.patch("/api/employees/{employee_id}/status")
def patch_employee_status(employee_id: int, status_data: schemas.StatusUpdate, db: Session = Depends(get_db)):
    db_employee = crud.update_employee_status(db, employee_id, status_data.status)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Status updated"}