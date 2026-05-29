from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
import models, schemas

# 生成默认工资明细
def get_default_wage_details():
    return [
        {"name": "基本工资", "type": "income", "amount": 8000},
        {"name": "绩效奖金", "type": "income", "amount": 2000},
        {"name": "社保扣款", "type": "deduction", "amount": 800},
        {"name": "餐补", "type": "income", "amount": 300},
    ]

# ── 登录认证 ──
def authenticate_employee(db: Session, name: str, password: str):
    user = db.query(models.Employee).filter(
        models.Employee.name == name,
        models.Employee.password == password
    ).first()
    return user

# ── 员工查询 ──
def get_employees(db: Session, status: str = None, search: str = None):
    query = db.query(models.Employee).options(joinedload(models.Employee.wage_details))
    if status and status != "all":
        query = query.filter(models.Employee.status == status)
    if search:
        query = query.filter(models.Employee.name.contains(search))
    return query.all()

def get_employee(db: Session, employee_id: int):
    return db.query(models.Employee)\
             .options(joinedload(models.Employee.wage_details))\
             .filter(models.Employee.id == employee_id).first()

# ── 员工自助：查询自己的工资条 ──
def get_my_wage(db: Session, employee_id: int):
    return db.query(models.Employee)\
             .options(joinedload(models.Employee.wage_details))\
             .filter(models.Employee.id == employee_id).first()

def create_employee(db: Session, employee: schemas.EmployeeCreate):
    employee_data = employee.model_dump(exclude={'wage_details'})
    db_employee = models.Employee(**employee_data)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)

    # 添加默认工资明细
    for wage_data in get_default_wage_details():
        wage = models.WageDetail(**wage_data, employee_id=db_employee.id)
        db.add(wage)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def update_employee(db: Session, employee_id: int, employee_update: schemas.EmployeeUpdate):
    db_employee = get_employee(db, employee_id)
    if not db_employee:
        return None

    update_data = employee_update.model_dump(exclude_unset=True)
    wage_details_data = update_data.pop("wage_details", None)

    # 更新基本信息
    for field, value in update_data.items():
        setattr(db_employee, field, value)

    # 更新工资明细（整体替换）
    if wage_details_data is not None:
        # 删除原有明细
        db.query(models.WageDetail).filter(models.WageDetail.employee_id == employee_id).delete()
        # 添加新明细
        for wage in wage_details_data:
            db_wage = models.WageDetail(**wage, employee_id=employee_id)
            db.add(db_wage)

    db.commit()
    db.refresh(db_employee)
    return db_employee

def update_employee_status(db: Session, employee_id: int, status: str):
    db_employee = get_employee(db, employee_id)
    if db_employee:
        db_employee.status = status
        db.commit()
        db.refresh(db_employee)
    return db_employee